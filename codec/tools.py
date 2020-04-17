import json
import os
from pkg.scalecodec import ScaleBytes
from pkg.scalecodec.base import ScaleDecoder, Singleton
from pkg.scalecodec.block import ExtrinsicsDecoder, EventsDecoder, LogDigest
from codec import MetadataInstant
from logger.conf import info
from pb import codec_pb2, codec_pb2_grpc
from pkg.scalecodec.base import RuntimeConfiguration
from utiles import websocket


class InvalidMetadataSpec(Exception):
    pass


class MetadataRegistry(metaclass=Singleton):
    registry = {}
    network = os.getenv("NETWORK_NODE", "darwinia")

    def __init__(self):
        module_path = os.path.dirname(__file__)
        path = os.path.join(module_path, 'metadata/{}.json'.format(self.network))
        with open(os.path.abspath(path), 'r') as fp:
            data = fp.read()
        j = json.loads(data)
        self.registry = ({"%s%s" % (self.network, spec): MetadataInstant(j[spec]) for spec in j})

    @classmethod
    def get_class_decoder(cls, spec):
        cl = MetadataRegistry().registry.get("%s%d" % (MetadataRegistry.network, spec), None)
        return cl.Decoder

    @classmethod
    def has_reg(cls, spec):
        class_string = "%s%d" % (MetadataRegistry.network, spec)
        return class_string in MetadataRegistry().registry

    @classmethod
    def reg_new_instant(cls, metadata, spec):
        if "%s%s" % (MetadataRegistry.network, spec) not in MetadataRegistry().registry:
            MetadataRegistry().registry["%s%s" % (MetadataRegistry.network, spec)] = MetadataInstant(metadata)


class Tools(codec_pb2_grpc.ToolsServicer):

    # block Extrinsic decode
    def DecodeExtrinsic(self, request, context):
        info("DecodeExtrinsic", (request.message, str(request.metadataVersion)))

        spec_ver = request.metadataVersion
        msg = json.loads(request.message)

        if MetadataRegistry().has_reg(spec_ver) is False:
            t = self.latest_decoder(spec_ver, request.blockHash)
        else:
            t = MetadataRegistry.get_class_decoder(spec_ver)

        result = []
        error = False
        RuntimeConfiguration().set_active_spec_version_id(spec_ver)
        for idx, extrinsic_data in enumerate(msg):
            extrinsic_decoder = ExtrinsicsDecoder(data=ScaleBytes(extrinsic_data), metadata=t)
            try:
                result.append(extrinsic_decoder.decode(False))
            except:
                error = True
        return codec_pb2.ExtrinsicReply(message=json.dumps(result), error=error)

    # block event decode
    def DecodeEvent(self, request, context):
        info('DecodeEvent', (request.message, str(request.metadataVersion)))

        spec_ver = request.metadataVersion

        if MetadataRegistry().has_reg(spec_ver) is False:
            t = self.latest_decoder(spec_ver, request.blockHash)
        else:
            t = MetadataRegistry.get_class_decoder(spec_ver)

        event = request.message
        RuntimeConfiguration().set_active_spec_version_id(spec_ver)
        events_decoder = EventsDecoder(data=ScaleBytes(event), metadata=t)
        result = []
        error = False
        try:
            result = events_decoder.decode(False)
        except:
            error = True
        return codec_pb2.EventReply(message=json.dumps(result), error=error)

    def DecodeLog(self, request, context):
        logs = json.loads(request.message)

        result = []
        if len(logs) == 0:
            return codec_pb2.ExtrinsicReply(message=json.dumps(result))
        info('DecodeLog', logs[0])
        for idx, log in enumerate(logs):
            log_decoder = LogDigest(data=ScaleBytes(log))
            result.append(log_decoder.decode(False))
        return codec_pb2.ExtrinsicReply(message=json.dumps(result))

    def DecodeStorage(self, request, context):
        info('DecodeStorage', (request.message, request.decoderType))

        msg = request.message
        spec_ver = request.metadataVersion
        decoder_type = request.decoderType

        RuntimeConfiguration().set_active_spec_version_id(spec_ver)

        if MetadataRegistry().has_reg(spec_ver) is False:
            t = self.latest_decoder(spec_ver)
        else:
            t = MetadataRegistry.get_class_decoder(spec_ver)
        obj = ScaleDecoder.get_decoder_class(decoder_type, ScaleBytes(msg), metadata=t)
        c = obj.decode(False)
        return codec_pb2.ExtrinsicReply(message=json.dumps(c))

    def RegMetadata(self, request, context):
        metadata = request.message
        spec_ver = str(request.metadataVersion)
        info('RegMetadata', (metadata, spec_ver))

        MetadataRegistry().reg_new_instant(metadata, spec_ver)
        return codec_pb2.ExtrinsicReply(message="true")

    @classmethod
    def latest_decoder(cls, spec_ver, block_hash=None):
        if block_hash is not None and os.getenv("NETWORK_ENDPOINT"):
            raw = websocket.get_current_metadata(os.getenv("NETWORK_ENDPOINT"), block_hash)
            if raw is not None:
                MetadataRegistry().reg_new_instant(raw, spec_ver)
                return MetadataRegistry.get_class_decoder(spec_ver)

        cl = MetadataRegistry().registry.get(sorted(MetadataRegistry().registry.keys())[-1], None)
        t = cl.Decoder
        return t

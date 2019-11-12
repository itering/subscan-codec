import json
import os
from scalecodec import ScaleBytes
from scalecodec.base import ScaleDecoder, Singleton
from scalecodec.block import ExtrinsicsDecoder, EventsDecoder, LogDigest
from codec import MetadataInstant
from logger.conf import info
from libs import rpc_pb2, rpc_pb2_grpc


class InvalidMetadataSpec(Exception):
    pass


class MetadataRegistry(metaclass=Singleton):
    registry = {}
    network = os.getenv("NETWORK_NODE", "darwinia")

    @classmethod
    def all_subclasses(cls, class_):
        return set(class_.__subclasses__()).union(
            [s for c in class_.__subclasses__() for s in cls.all_subclasses(c)])

    def __init__(self):
        self.registry = ({cls.__name__.lower(): cls for cls in self.all_subclasses(MetadataInstant)})

    @classmethod
    def get_class_decoder(cls, spec):
        cl = MetadataRegistry().registry.get("%s%dinstant" % (MetadataRegistry().network, spec), None)
        return cl().Decoder

    @classmethod
    def has_reg(cls, spec):
        class_string = "%s%dinstant" % (MetadataRegistry().network, spec)
        return class_string in MetadataRegistry().registry


class Tools(rpc_pb2_grpc.ToolsServicer):

    def DecodeExtrinsic(self, request, context):
        info("DecodeExtrinsic", (request.message, str(request.metadataVersion)))
        spec_ver = request.metadataVersion
        if MetadataRegistry.has_reg(spec_ver) is False:
            raise InvalidMetadataSpec
        msg = json.loads(request.message)
        t = MetadataRegistry.get_class_decoder(spec_ver)
        result = []
        for idx, extrinsic_data in enumerate(msg):
            extrinsic_decoder = ExtrinsicsDecoder(data=ScaleBytes(extrinsic_data), metadata=t)
            result.append(extrinsic_decoder.decode(False))
        return rpc_pb2.ExtrinsicReply(message=json.dumps(result))

    def DecodeEvent(self, request, context):
        info('DecodeEvent', (request.message, str(request.metadataVersion)))
        spec_ver = request.metadataVersion
        if MetadataRegistry.has_reg(spec_ver) is False:
            raise InvalidMetadataSpec
        event = request.message
        t = MetadataRegistry.get_class_decoder(spec_ver)
        events_decoder = EventsDecoder(data=ScaleBytes(event), metadata=t)
        return rpc_pb2.EventReply(message=json.dumps(events_decoder.decode(False)))

    def DecodeLog(self, request, context):
        logs = json.loads(request.message)
        info('DecodeLog', logs[0])
        result = []
        for idx, log in enumerate(logs):
            log_decoder = LogDigest(data=ScaleBytes(log))
            result.append(log_decoder.decode(False))
        return rpc_pb2.ExtrinsicReply(message=json.dumps(result))

    def DecodeStorage(self, request, context):
        info('DecodeStorage', (request.message, request.decoderType))
        msg = request.message
        decoder_type = request.decoderType
        obj = ScaleDecoder.get_decoder_class(decoder_type, ScaleBytes(msg))
        c = obj.decode(False)
        return rpc_pb2.ExtrinsicReply(message=json.dumps(c))

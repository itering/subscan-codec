import json

from scalecodec import ScaleBytes
from scalecodec.base import ScaleDecoder
from scalecodec.block import ExtrinsicsDecoder, EventsDecoder, LogDigest

from libs import rpc_pb2, rpc_pb2_grpc
from codec import MetadataV6Instant, MetadataKusamaInstant, MetadataKusama1006Instant, \
    MetadataKusama1008Instant, MetadataKusama1010Instant, MetadataKusama1011Instant, MetadataKusama1012Instant, \
    MetadataKusama1015Instant, MetadataKusama1016Instant


class Tools(rpc_pb2_grpc.ToolsServicer):
    MetadataDecoderInstantMap = {
        78: MetadataV6Instant(),
        1003: MetadataKusamaInstant(),
        1006: MetadataKusama1006Instant(),
        1008: MetadataKusama1008Instant(),
        1010: MetadataKusama1010Instant(),
        1011: MetadataKusama1011Instant(),
        1012: MetadataKusama1012Instant(),
        1015: MetadataKusama1015Instant(),
        1016: MetadataKusama1016Instant(),
    }

    def DecodeExtrinsic(self, request, context):
        msg = json.loads(request.message)
        metadata_version = request.metadataVersion
        while metadata_version not in self.MetadataDecoderInstantMap:
            metadata_version -= 1
        m = self.MetadataDecoderInstantMap[metadata_version]
        result = []
        for idx, extrinsic_data in enumerate(msg):
            extrinsic_decoder = ExtrinsicsDecoder(data=ScaleBytes(extrinsic_data), metadata=m.Decoder)
            result.append(extrinsic_decoder.decode(False))
        return rpc_pb2.ExtrinsicReply(message=json.dumps(result))

    def DecodeEvent(self, request, context):
        event = request.message
        metadata_version = request.metadataVersion
        while metadata_version not in self.MetadataDecoderInstantMap:
            metadata_version -= 1
        m = self.MetadataDecoderInstantMap[metadata_version]
        events_decoder = EventsDecoder(data=ScaleBytes(event), metadata=m.Decoder)
        return rpc_pb2.EventReply(message=json.dumps(events_decoder.decode(False)))

    def DecodeLog(self, request, context):
        logs = json.loads(request.message)
        result = []
        for idx, log in enumerate(logs):
            log_decoder = LogDigest(data=ScaleBytes(log))
            result.append(log_decoder.decode(False))
        return rpc_pb2.ExtrinsicReply(message=json.dumps(result))

    def DecodeStorage(self, request, context):
        msg = request.message
        decoder_type = request.decoderType
        obj = ScaleDecoder.get_decoder_class(decoder_type, ScaleBytes(msg))
        c = obj.decode(False)
        return rpc_pb2.ExtrinsicReply(message=json.dumps(c))

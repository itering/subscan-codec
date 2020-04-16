import os
import grpc

from concurrent import futures
from pkg.scalecodec.base import RuntimeConfiguration
from codec.tools import Tools
from pb import codec_pb2_grpc
from type_registry import load_type_registry
from logger.conf import log_config, LOGGER
from codec.tools import MetadataRegistry


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), compression=grpc.Compression.Gzip)
    codec_pb2_grpc.add_ToolsServicer_to_server(Tools(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    LOGGER.info("SubScan Tools server start :50051")
    server.wait_for_termination()


def type_registry():
    RuntimeConfiguration().update_type_registry(load_type_registry("default"))
    RuntimeConfiguration().update_type_registry(load_type_registry(os.getenv("NETWORK_NODE", "canary")))
    MetadataRegistry()


if __name__ == '__main__':
    log_config()
    type_registry()
    serve()

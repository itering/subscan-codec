import os

import time
from concurrent import futures

import grpc
from scalecodec.base import RuntimeConfiguration

from codec.tools import Tools
from libs import rpc_pb2_grpc
from type_registry import load_type_registry
from logger.conf import log_config, LOGGER

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc_pb2_grpc.add_ToolsServicer_to_server(Tools(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    LOGGER.info("SubScan Tools server start :50051")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def type_registry():
    RuntimeConfiguration().update_type_registry(load_type_registry("default"))
    if os.getenv("NETWORK_NODE") == "kusama":
        RuntimeConfiguration().update_type_registry(load_type_registry("kusama"))
    elif os.getenv("NETWORK_NODE") == "darwinia":
        RuntimeConfiguration().update_type_registry(load_type_registry("darwinia"))


if __name__ == '__main__':
    log_config()
    type_registry()
    serve()

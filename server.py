import logging
import os
import sys
import time
from concurrent import futures

import grpc
from scalecodec.base import RuntimeConfiguration

from codec import Tools
from libs import rpc_pb2_grpc
from type_registry import load_type_registry

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_LOGGER = logging.getLogger(__name__)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc_pb2_grpc.add_ToolsServicer_to_server(Tools(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    _LOGGER.info("darwinia tools server start :50051")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def type_registry():
    if os.getenv("NETWORK_NODE") == "kusama":
        RuntimeConfiguration().update_type_registry(load_type_registry("kusama"))


def log_config():
    logging.basicConfig()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.DEBUG)


if __name__ == '__main__':
    type_registry()
    serve()

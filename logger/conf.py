import logging
import coloredlogs

LOGGER = logging.getLogger(__name__)


def log_config():
    coloredlogs.install()
    logging.basicConfig()
    LOGGER.setLevel(logging.DEBUG)


def info(method, params):
    LOGGER.info("{} -- {}".format(method, "".join(set(list(map(lambda x: x[:30], params))))))
    pass

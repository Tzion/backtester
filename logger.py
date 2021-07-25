import logging
import sys

ROOT_LOG_LEVEL = logging.INFO

logging.LoggerAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(process)s-%(thread)s %(name)s %(levelname)s: %(message)s', datefmt='%y-%m-%d_%H:%M:%S'))
handler.setStream(sys.stdout)
logger.addHandler(handler)

def logdebug(message):
    logger.info("bueas")


def logdebugdeco(message):
    logdebug(message)
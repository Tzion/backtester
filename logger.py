import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(process)s-%(thread)s %(name)s %(levelname)s:  %(message)s', datefmt='%y-%m-%d_%H:%M:%S'))
handler.setStream(sys.stdout)
logger.addHandler(handler)


def logdebug(message, feed=None):
    logger.debug(inject_feed(message, feed))

def inject_feed(message, feed):
    if feed:
        try:
            name = feed._name
            time = feed.datetime.date()
            message = f'[{name}@{time}] {message}'
        except Exception as e:
            message = f'[ERROR] {message}'
    return message
        

def logdebugdeco(message):
    logdebug(message)


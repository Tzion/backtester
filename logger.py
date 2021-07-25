import logging
import logging.config
import sys


# root_logger = logging.getLogger()
# root_logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter(fmt='%(asctime)s %(process)s-%(thread)s %(name)s %(levelname)s:  %(message)s', datefmt='%y-%m-%d_%H:%M:%S')
# file_handler = logging.FileHandler('./log1.log', 'w')
# file_handler.setFormatter(formatter)
# root_logger.addHandler(file_handler)

# logger = logging.getLogger('backtester')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler()
# handler.setFormatter(formatter)
# handler.setStream(sys.stdout)
# logger.addHandler(handler)

logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger('backtester')


def logdebug(message, feed=None):
    logger.debug(inject_feed(message, feed))
    pass

def loginfo(message, feed=None):
    logger.info(inject_feed(message, feed))

def logwarning(message, feed=None):
    logger.warning(inject_feed(message, feed))

def logerror(message, feed=None):
    logger.exception(inject_feed(message, feed))

def logcritical(message, feed=None):
    logger.critical(inject_feed(message, feed))

def inject_feed(message, feed):
    if feed:
        try:
            name = feed._name
            time = feed.datetime.date()
            message = f'[{name}@{time}] {message}'
        except Exception as e:
            message = f'[ERROR] {message}'
    return message
        
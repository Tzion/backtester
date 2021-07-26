import logging
import logging.config

logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)

logger = logging.getLogger('backtester')  # must be same string as qualname value inside the .conf file

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
            message = f'[{name} @ {time}] {message}'
        except Exception as e:
            message = f'[FEEDERROR] {message}'
    return message
        
import logging
import sys

class FeedAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        if 'extra' in kwargs and 'feed_name' in kwargs['extra']:
            msg = f"{kwargs['extra']['feed_name']} {msg}"
        return msg,kwargs

class ContextFilter(logging.Filter):

    def filter(self, record):
        record.feed = "MYFEED"
        # record.feedtime = '12'
        return True

logging.LoggerAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(process)s-%(thread)s %(name)s %(levelname)s: %(message)s', datefmt='%y-%m-%d_%H:%M:%S'))
handler.setStream(sys.stdout)
logger.addHandler(handler)
# logger.addFilter(ContextFilter())
# extra = {'feed_name':'DEFAULT'}
extra = {}

logger = FeedAdapter(logger, extra)


def logdebug(message, feed=None):
    logger.debug(message, extra=extract_feed(feed))

def extract_feed(feed):
    extra = {'feed_name':'', 'feedtime':''}
    if feed:
        try: 
            extra['feed_name']= feed._name
            extra['feedtime']= feed.datetime.date()
        except Exception as e:
           extra['feed_name'] = 'ERROR' 
    return extra


def logdebugdeco(message):
    logdebug(message)


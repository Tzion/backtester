import logging
import sys

class FeedAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        if self.extra['feedtime'] == '':
            return "manipulating the message", kwargs
        return msg,kwargs

logging.LoggerAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(process)s-%(thread)s %(name)s %(levelname)s: [%(feed)s@%(feedtime)s] %(message)s', datefmt='%y-%m-%d_%H:%M:%S'))
handler.setStream(sys.stdout)
logger.addHandler(handler)
extra = {'feed':'', 'feedtime':''}
logger = FeedAdapter(logger, extra)


def logdebug(message, feed=None):
    logger.debug(message, extra=extract_feed(feed))

def extract_feed(feed):
    extra = {'feed':'', 'feedtime':''}
    if feed:
        try: 
            extra['feed']= feed._name
            extra['feedtime']= feed.datetime.date()
        except Exception as e:
           extra['feed'] = 'ERROR' 
    return extra


def logdebugdeco(message):
    logdebug(message)


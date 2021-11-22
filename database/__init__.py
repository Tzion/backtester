import sys
import enum

PROD_FLAG = '--prod'

class DatabaseEnv(enum.Enum):
    TESTING, PRODUCTION = range(1,3)

    @classmethod
    def get(cls):
        return DATABASE_ENV.value

    @classmethod
    def get_name(cls):
        return DATABASE_ENV.name

DATABASE_ENV = DatabaseEnv.TESTING

if PROD_FLAG in sys.argv:
    DATABASE_ENV = DatabaseEnv.PRODUCTION
    

def get_stored_feed_file_path(symbol):
    pass
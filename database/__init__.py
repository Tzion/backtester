import sys

PROD_FLAG = '--prod'

class DatabaseEnv:
    TESTING, PRODUCTION = range(1,3)

    @classmethod
    def get(cls):
        return ENV

    @classmethod
    def get_name(cls):
        return list(DatabaseEnv.__dict__.keys())[ENV]

ENV = DatabaseEnv.TESTING

if PROD_FLAG in sys.argv:
    ENV = DatabaseEnv.PRODUCTION
    

def get_stored_feed_file_path(symbol):
    pass
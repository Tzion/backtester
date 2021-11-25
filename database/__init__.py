import sys
import os
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
    

def get_feed_file_path(symbol):
    path = f'database/{DatabaseEnv.get_name()}/data_feeds/{symbol}.csv'
    if os.path.isfile(path):
        return path
    return None

    
    """"static database desired structre:
    Option A:
    root -> <Environment> -> <symbol> -> :
                                            [metadata]: Symbol, Contract type, Exchange, Currency, Market, Sector,
                                            [data]: Price & Volume,

    Option B:
    root -> <Environment> -> Searchable criterias:
                                            [metadata]: Symbol, Contract type, Exchange, Currency, Market, Sector, Path
                            Data files:
                                            Price & Volume,
    
                                            
    """
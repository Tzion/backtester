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
    
# %%
    
file_1 = 'TESTING/trading_view/22lines.csv'
file_2 = 'TESTING/trading_view/22lines_missing_date_middle.csv'

def diff_data_feed_csv(file_1, file_2, columns=['open', 'low', 'high', 'close',]):
    # TODO support date range
    df1 = pd.read_csv(file_1, parse_dates=[0])
    df2 = pd.read_csv(file_2, parse_dates=[0])
    columns.insert(0,df1.columns[0])
    df1 = pd.DataFrame(df1, columns=columns)
    df2 = pd.DataFrame(df2, columns=columns)
    equal = df1.eq(df2)
    if equal.all().all():
        return False  # no diffs between dataframes
    else:
        return equal
    # to show details results - next phase
    compare = df11[df11.eq(df22).all(axis=1) == False]
    print(comparison.to_string(index=True))


# %%
import pandas as pd

# %%
columns = ['open', 'low']

# %%
df1 = pd.read_csv(file_1, parse_dates=[0])
df2 = pd.read_csv(file_2, parse_dates=[0])
#%%
columns.insert(0,df1.columns[0])
df11 = pd.DataFrame(df1, columns=columns)
df22 = pd.DataFrame(df2, columns=columns)
    
# %%
df11.eq(df22)
# %%
comparison = df11[df11.eq(df22).all(axis=1) == False]
print(comparison.to_string(index=True))

# %%

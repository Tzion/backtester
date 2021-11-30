from pathlib import Path
import os
import enum
import pandas as pd

class DataSource(enum.Enum):
    INTERACTIVE_BROKERS = 1
    TRADING_VIEW = 2
    YAHOO = 3

    def get_name(self):
        return self.name.lower()


def get_feed_file_path(symbol, source: DataSource=DataSource.INTERACTIVE_BROKERS):
    def find_file(symbol, dir):
        matches = list(Path(dir).glob('*.csv'))
        if len(matches) > 1:
            raise Exception('Ambiguos search results: more than 1 files matches the symbol')
        return str(matches[0])
        
    dir = f'database/{source.get_name()}/'
    path = find_file(symbol, dir)
    if os.path.isfile(path):
        return path
    return None

    
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

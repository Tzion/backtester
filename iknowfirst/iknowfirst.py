import pandas as pd
import numpy as np
import os
from datetime import datetime
from typing import Optional


FORECASTS_FOLDER = 'iknowfirst/ikf_forecasts/'
forecasts : pd.DataFrame = None
CACHE_FILE = 'cache.pkl'

def extract_data_from_file(file_path):
    def extract_from_sheet(sheet_name, keys):
        file_dataframe = pd.read_excel(file_path, sheet_name=sheet_name)
        table_dataframes = []
        for table_range in range(1, 19,6):
            table_dataframe = pd.DataFrame()
            for row_range in range(4,24,3):
                row = file_dataframe.iloc[row_range:row_range+3, table_range:table_range+5]
                row_df = pd.DataFrame(data=row.iloc[1:].values.T, index=row.iloc[:1].values[0], columns=[
                                  'strength', 'predictability'])
                row_df = row_df[~ row_df.index.isna()]  # filter out row with nan on the index
                table_dataframe = pd.concat([table_dataframe, row_df])
                # table_dataframe.sort_values(by=['strength', 'predictability'], ascending=False, inplace=True) # no need since the tables come sorted
            table_dataframes.append(table_dataframe)
        return pd.concat(table_dataframes, keys=keys)

    dataframes = extract_from_sheet('3-7-14days', ['3days', '7days', '14days']), extract_from_sheet('1-3-12months',['1months', '3months', '12months'])
    return pd.concat(dataframes)

# design bug - scenario: 2 calls- use_cache=True then False - in the second call the dataframe returned is the one theat was load from the cache on the first call
def retrieve_forecasts_data(forecasts_folder=FORECASTS_FOLDER, use_cache=True, filter_friday=True):
    if use_cache :
        load_from_cache()
    global forecasts
    if forecasts is None:
        print("Retrieving forecasts data")
        files = list(map(lambda file: forecasts_folder + '/' + file, os.listdir(forecasts_folder)))
        files = list(filter(lambda name: name.endswith('.xls'), files))
        dataframes = []
        dates = []
        for f in files:
            dataframes.append(extract_data_from_file(f))
            dates.append(datetime.strptime(f[f.find('TA35_')+5:-4],'%d_%b_%Y'))
        dataframe = pd.concat(dataframes, keys=dates)
        forecasts = dataframe.sort_index(axis='index', level=None, sort_remaining=True)
        dataframe.index.set_names(['date', 'timeframe', 'stock'], inplace=True)
    forecasts.drop_duplicates(keep='first', inplace=True)
    save_to_cache(forecasts)
    return forecasts.loc[filter(lambda i: i[0].dayofweek != 4, forecasts.index)] if filter_friday else forecasts

def load_from_cache():
    '''## todo check modification time and make sure to use relevant file
    os.path.getmtime
    os.path.getctime
    pd.read_pickle(FORECASTS_FOLDER + CACHE_FILE)
    '''
    global forecasts
    try:
        cache = pd.read_pickle(FORECASTS_FOLDER + CACHE_FILE)
        forecasts = cache
        return True 
    except FileNotFoundError as e:
        return False

def save_to_cache(dataframe: pd.DataFrame):
    pd.to_pickle(dataframe, FORECASTS_FOLDER + CACHE_FILE)

def retrieve_stocks():
    global forecasts
    if forecasts is None:
        retrieve_forecasts_data()
    return list({i[2] for i in forecasts.index})


def get_forecast_on(date, timeframe=None) -> Optional[pd.DataFrame]:
    global forecasts
    if timeframe: 
        return forecasts.loc[str(date), timeframe] 
    else:
        return forecasts.loc[str(date),]

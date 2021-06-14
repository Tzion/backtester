import pandas as pd
import numpy as np
import os
from datetime import datetime

from pandas.core.accessor import CachedAccessor

FORECASTS_FOLDER = 'iknowfirst/ikf_forecasts/'
forecasts = None
CACHE_FILE = 'cache.pkl'

def extract_data_from_file(file_path):
    def extract_from_sheet(sheet_name, keys):
        dataframe = pd.read_excel(file_path, sheet_name=sheet_name)
        dataframes = []
        for i in range(1, 19,6):
            df_top = dataframe.iloc[4:7, i:i+5]
            df_top = pd.DataFrame(data=df_top.iloc[1:].values.T, index=df_top.iloc[:1].values[0], columns=[
                                  'strength', 'predictability'])
            dataframes.append(df_top)
        return pd.concat(dataframes, keys=keys)

    dataframes = extract_from_sheet('3-7-14days', ['3days', '7days', '14days']), extract_from_sheet('1-3-12months',['1months', '3months', '12months'])
    return pd.concat(dataframes)

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
        forecasts = dataframe.sort_index(axis='index', level=0, sort_remaining=True)
        dataframe.index.set_names(['date', 'timeframe', 'stock'], inplace=True)
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

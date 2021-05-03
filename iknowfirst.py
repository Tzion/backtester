import pandas as pd
import numpy as np
import os
from datetime import datetime

FORECASTS_FOLDER = './ikf_forecasts'
TRADINGVIEW_CSV_FORMAT = lambda s: 'TASE_DLY_' + s.replace('.TA', '') + ', 1D.csv'

def extract_data_from_file(file_path):
    def extract_from_sheet(sheet_name, keys):
        dataframe = pd.read_excel(file_path, sheet_name=sheet_name)
        dataframes = []
        for i in range(1, 19,6):
            df_top = dataframe.iloc[4:7, i:i+5]
            df_top = pd.DataFrame(data=df_top.iloc[1:].values.T, index=df_top.iloc[:1].values[0], columns=['strength', 'predictability'])
            dataframes.append(df_top)
        return pd.concat(dataframes, keys=keys)

    dataframes = extract_from_sheet('3-7-14days', ['3days', '7days', '14days']), extract_from_sheet('1-3-12months',['1months', '3months', '12months'])
    return pd.concat(dataframes)

def retrieve_forecasts_data(forecasts_folder=FORECASTS_FOLDER):
    print("Retrieving forecasts data")
    files = list(map(lambda file: forecasts_folder + '/' + file, os.listdir(forecasts_folder)))
    dataframes = []
    dates = []
    for f in files:
        dataframes.append(extract_data_from_file(f))
        dates.append(datetime.strptime(f[f.find('TA35_')+5:-4],'%d_%b_%Y'))
    dataframe = pd.concat(dataframes, keys=dates)
    return dataframe.sort_index(axis='index', level=0, sort_remaining=True)


ikf_forecasts = None

def retrieve_stocks(adapter=TRADINGVIEW_CSV_FORMAT):
    global ikf_forecasts
    if ikf_forecasts is None:
        ikf_forecasts = retrieve_forecasts_data()
    stocks = {i[2] for i in ikf_forecasts.index}
    return list(stocks) if adapter is None else list(map(adapter,stocks))
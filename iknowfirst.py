#%%
import pandas as pd
import xlrd
import numpy as np

def extract_data(sheet_name, timeframe_keys):
    messy = pd.read_excel('ikf/IKForecast_big_Israel_top_5_TA35_20_Apr_2021.xls', sheet_name=sheet_name)
    dataframes = []
    for i in range(1, 19,6):
        df_top = messy.iloc[4:7, i:i+5]
        df_top = pd.DataFrame(data=df_top.iloc[1:].values.T, index=df_top.iloc[:1].values[0], columns=['strength', 'predictability'])
        dataframes.append(df_top)
    return pd.concat(dataframes,keys=timeframe_keys)
# %%
sheets = [('3-7-14days', ['3days', '7days', '14days']), ('1-3-12months', ['1months', '3months', '12months'])]
output = [extract_data(*sheets[0]), extract_data(*sheets[1])]
output = pd.concat(output)

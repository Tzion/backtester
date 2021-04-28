#%%
import pandas as pd
import xlrd
import numpy as np

messy = pd.read_excel('ikf/IKForecast_big_Israel_top_5_TA35_20_Apr_2021.xls', sheet_name='3-7-14days')
dataframes = []
for i in range(1, 19,6):
    df_top = messy.iloc[4:7, i:i+5]
    df_top = pd.DataFrame(data=df_top.iloc[1:].values.T, index=df_top.iloc[:1].values[0], columns=['strength', 'predictability'])
    dataframes.append(df_top)
tidy = pd.concat(dataframes, keys=['3days', '7days', '14days'])
# %%

df_month = pd.read_excel('ikf/IKForecast_big_Israel_top_5_TA35_20_Apr_2021.xls', sheet_name='1-3-12months')
df1_top = df.iloc[4:7, 1:6]
# %%

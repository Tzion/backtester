#%%
import pandas as pd
import xlrd
import numpy as np

#%% 
df = pd.read_excel('ikf/IKForecast_big_Israel_top_5_TA35_20_Apr_2021.xls')
df1_top = df.iloc[4:7, 1:6]
df1_top = pd.DataFrame(data=df1_top.iloc[1:].values.T, index=df1_top.iloc[:1].values[0], columns=['strength', 'predictability'])
# %%

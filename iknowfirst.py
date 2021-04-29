#%%
import pandas as pd
import numpy as np

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

    
output = extract_data_from_file('ikf_forecasts/IKForecast_big_Israel_top_5_TA35_20_Apr_2021.xls')

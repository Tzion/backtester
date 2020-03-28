import pandas as pd
import pandas_datareader as pdr
import os

data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = data[0]
tickers = table['Symbol'].tolist()

# todo validate data_feed directory
lost = []
for symbol in tickers:
    try:
        if not os.path.exists('./data_feeds/{}.csv'.format(symbol)):
            print('downloading data feed of {}'.format(symbol))
            feed = pdr.get_data_yahoo(symbol.replace('.',''))
            feed.to_csv('./data_feeds/{}.csv'.format(symbol))
        else:
            print('data feed of {} already exists, skipping'.format(symbol))
    except:
        lost.append(symbol)  
if len(lost) is not 0:
    print("\033[31mError downloading symbols: {}.\033[00m".format(lost))

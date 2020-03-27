import pandas as pd
import pandas_datareader as pdr
import os

data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = data[0]
tickers = table['Symbol'].tolist()

# todo validate data_feed directory
for symbol in tickers:
    if not os.path.exists('./data_feeds/{}.csv'.format(symbol)):
        print('downloading data feed of {}'.format(symbol))
        feed = pdr.get_data_yahoo(symbol)
        feed.to_csv('./data_feeds/{}.csv'.format(symbol))
    else:
        print('data feed of {} already exists, skipping'.format(symbol))

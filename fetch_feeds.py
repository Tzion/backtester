import pandas as pd
import os
import yfinance as yf

data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = data[0]
tickers = table['Symbol'].tolist()
FEEDS_DIR = './data_feeds/'

# todo validate data_feed directory
lost = []
for symbol in tickers:
    try:
        if not os.path.exists(f'{FEEDS_DIR}{symbol}.csv'):
            print('downloading data feed of {}'.format(symbol))
            symbol = symbol.replace('.','')
            feed = yf.download(symbol, start=None, end=None, progress=True) #  when start and end are None gives all histroy until today.
            feed.to_csv(f'{FEEDS_DIR}{symbol}.csv')
        else:
            print('data feed of {} already exists, skipping'.format(symbol))
    except Exception as e:
        print(e)
        lost.append(symbol)  
if len(lost):
    print("\033[31mError downloading {} symbols: {}.\033[00m".format(len(lost), lost))

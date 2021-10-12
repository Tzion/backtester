import backtrader as bt
import math

cerebro = bt.Cerebro()

OUTPUT_DIR = 'output/'
# TODO move to charts package
CHARTS_DIR = OUTPUT_DIR + 'charts/'
OBSERVERS_DIR = CHARTS_DIR + 'observers/'
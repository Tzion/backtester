import backtrader as bt
import os
import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DummyStrategy(bt.Strategy):
    pass
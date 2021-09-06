import backtrader as bt
import os
import os.path
import sys
import pandas as pd
import pytest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) # TODO no need anymore - remove after align all test classes
from backtrader.feeds.pandafeed import PandasData

class DummyStrategy(bt.Strategy):
    pass

DUMMY_DATA = PandasData(dataname=pd.DataFrame(data=1, columns=PandasData.datafields, index=pd.date_range('20210816', periods=10)))
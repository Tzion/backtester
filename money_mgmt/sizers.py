import backtrader as bt

class PortionSizer(bt.Sizer):

    def __init__(self, percents=10.0):
        self.percents= percents

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        account = self.broker.getvalue()
        if not position:
            size = account / data.close[0] * (self.percents / 100)
        else:
            size = position.size # should I return -1*size to indicate that it's opposite direction?

        return int(size)

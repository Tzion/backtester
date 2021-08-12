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
            size = position.size

        return size


class LongOnlyPortionSizer(PortionSizer):
    '''
    Do not use on bracket orders
    '''
    def _getsizing(self, comminfo, cash, data, isbuy):
        if not isbuy and not self.broker.getposition(data):
            return 0
        return super()._getsizing(comminfo, cash, data, isbuy)

class RiskBasedSizer(bt.Sizer):

    def __init__(self, risk_per_trade_percents=2.0):
        self.risk_per_trade = risk_per_trade_percents/100

    def _getsizing(self, comminfo, cash, data, isbuy):
        risk = getattr(data, 'risk')
        if not risk and not callable(risk):
            raise Exception(f'{self.__class__.__name__} sizer requires {data} to have risk() method')

        position = self.broker.getposition(data)
        if position:
            return position.size

        size = (self.risk_per_trade * self.broker.getvalue()) / data.risk()
        return size
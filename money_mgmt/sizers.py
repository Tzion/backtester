import backtrader as bt

class PortionSizer(bt.Sizer):

    def __init__(self, percents=10.0):
        self.percents= percents

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        account = self.broker.getvalue()
        if not position:
            size = account / data.close[0] * (self.percents / 100)  # there's an assumption that the asked priced is today's close price (data.close[0])
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


class RiskBasedWithMaxPortionSizer(RiskBasedSizer):

    def __init__(self, risk_per_trade_percents, max_portion_percents):
        super().__init__(risk_per_trade_percents)
        self.portion_sizer = PortionSizer(percents=max_portion_percents)
    
    def _getsizing(self, comminfo, cash, data, isbuy):
        return min(super()._getsizing(comminfo, cash, data, isbuy), self.portion_sizer._getsizing(comminfo, cash, data, isbuy))

    def set(self, strategy, broker):
        super().set(strategy, broker)
        self.portion_sizer.set(strategy, broker)
from strategies.trade_phase_strategy import TradeState, TradeStateStrategy


class TradePhaseStrategyTest(TradeStateStrategy):
    def __init__(self):
        super().__init__(TradePhaseTest)


class TradePhaseTest(TradeState):

    def next(self):
        print('next() Trade Phase Test for feed %s'%self.feed._name)
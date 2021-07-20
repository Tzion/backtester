from strategies.trade_state_strategy import TradeState, TradeStateStrategy


class TradePhaseStrategyTest(TradeStateStrategy):

    def initial_state_cls(self):
        return TradePhaseTest


class TradePhaseTest(TradeState):

    def next(self):
        print('next() Trade Phase Test for feed %s'%self.feed._name)
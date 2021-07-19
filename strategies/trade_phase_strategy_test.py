from .trade_phase_strategy import TradePhase, TradePhaseStrategy

# TODO move to test area

class TradePhaseStrategyTest(TradePhaseStrategy):
    def __init__(self):
        super().__init__(TradePhaseTest)


class TradePhaseTest(TradePhase):

    def next(self):
        print('next() Trade Phase Test for feed %s'%self.feed._name)
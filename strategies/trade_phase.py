from __future__ import annotations
import strategies.trade_phase_strategy as trade_phase_strategy
class TradePhase():

    strategy : trade_phase_strategy.TradePhaseStrategy

    def __init__(self, strategy : trade_phase_strategy.TradePhaseStrategy, feed):
        self.strategy = strategy
        self.feed = feed
    
    def next(self):
        NotImplementedError

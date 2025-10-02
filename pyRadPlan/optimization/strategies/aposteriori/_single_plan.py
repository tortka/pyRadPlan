import numpy as np
from ._base import TradeoffStrategyBase


class SinglePlan(TradeoffStrategyBase):
    name = "Single Plan Tradeoff Strategy"
    short_name = "single"
    apriori_strategy = "WeightedSum"

    def _solve(self, x: np.ndarray[float]) -> list[np.ndarray[float]]:
        return self.apriori_strategy.solve(x)

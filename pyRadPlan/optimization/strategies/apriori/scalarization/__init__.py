"A module for scalarization strategies."

from .._factory import register_apriori_strategy
from ._weighted_sum import WeightedSumOptimization

register_apriori_strategy(WeightedSumOptimization)


__all__ = [
    "WeightedSumOptimization"
    ]

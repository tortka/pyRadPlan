"A module for lexicographic strategies."

from .._factory import register_apriori_strategy
from ._lexicographic import LexicographicOptimization

register_apriori_strategy(LexicographicOptimization)


__all__ = [
    "LexicographicOptimization"
    ]

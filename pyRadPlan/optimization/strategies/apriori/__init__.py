"A module for a priori optimization strategies."

from ._base import APrioriStrategyBase
from ._factory import (
    get_available_apriori_strategies,
    get_apriori_strategy,
    register_apriori_strategy
    )

from . import lexicographic
from . import scalarization


__all__ = [
    "APrioriStrategyBase",
    "get_available_apriori_strategies",
    "get_apriori_strategy",
    "register_apriori_strategy",
    "lexicographic",
    "scalarization"
    ]

"Lexicographic optimization class."

from typing import Union
import numpy as np
import logging


from .._base import APrioriStrategyBase

logger = logging.getLogger(__name__)


class LexicographicOptimization(APrioriStrategyBase):
    "."
    name = "Lexicographic optimization"
    short_name = "lexicographic"
    weights: Union[np.ndarray[float], list[float], None]
    
    def __init__(self):
        pass

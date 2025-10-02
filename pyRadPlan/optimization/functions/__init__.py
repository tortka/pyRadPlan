"""A module for the optimization functions."""

from ._function import Function
from ._std import DoseUniformity
from ._eud import EUD
from ._max_dvh import MaxDVH
from ._mean import MeanDose
from ._min_dvh import MinDVH
from ._squared_dev import SquaredDeviation
from ._squared_over import SquaredOverdosing
from ._squared_under import SquaredUnderdosing

from ._factory import get_available_functions, get_function, register_function

register_function(DoseUniformity)
register_function(EUD)
register_function(MaxDVH)
register_function(MeanDose)
register_function(MinDVH)
register_function(SquaredDeviation)
register_function(SquaredOverdosing)
register_function(SquaredUnderdosing)

__all__ = [
    "Function",
    "DoseUniformity",
    "EUD",
    "MaxDVH",
    "MeanDose",
    "MinDVH",
    "SquaredDeviation",
    "SquaredOverdosing",
    "SquaredUnderdosing",
    "get_available_functions",
    "get_function",
    "register_function",
]

"""Factory methods to manage available function implementations."""

import warnings
import logging
from typing import Union, Type
from ._function import Function

__matrad_name_map__ = {
    "DoseObjectives.matRad_SquaredDeviation": "Squared Deviation",
    "DoseObjectives.matRad_SquaredUnderdosing": "Squared Underdosing",
    "DoseObjectives.matRad_SquaredOverdosing": "Squared Overdosing",
    "DoseObjectives.matRad_MeanDose": "Mean Dose",
    "DoseObjectives.matRad_EUD": "EUD",
    "DoseObjectives.matRad_MinDVH": "MinDVH",
    "DoseObjectives.matRad_MaxDVH": "MaxDVH",
}

FUNCTIONS = {}

logger = logging.getLogger(__name__)


def register_function(func_cls: Type[Function]) -> None:
    """
    Register a new function.

    Parameters
    ----------
    obj_cls : type
        A Function class.
    """
    if not issubclass(func_cls, Function):
        raise ValueError("Function must be a subclass of Function.")

    if func_cls.name is None:
        raise ValueError("Function must have a 'name' attribute.")

    func_name = func_cls.name
    if func_name in FUNCTIONS:
        warnings.warn(f"Function '{func_name}' is already registered.")
    else:
        FUNCTIONS[func_name] = func_cls


def get_available_functions() -> dict[str, Type[Function]]:
    """
    Get a list of available functions.

    Returns
    -------
    list
        A list of available functions.
    """
    return FUNCTIONS


def get_function(function_desc: Union[str, dict, Function]):
    """
    Returns a function instance based on a descriptive parameter.

    Parameters
    ----------
    function_desc : Union[str, dict, Function]
        A string with the function name, a dictionary with the function configuration or a
        function instance

    Returns
    -------
    Objective
        A function instance
    """
    if isinstance(function_desc, str):
        function = FUNCTIONS[function_desc]()
    elif isinstance(function_desc, dict):
        if "name" not in function_desc:
            logger.debug("Function not found, trying matRad-like function.")
            if "className" not in function_desc:
                raise ValueError(f"Invalid function description: {function_desc}")
            function_name = __matrad_name_map__.get(function_desc["className"], None)
            if function_name is None:
                raise ValueError(f"Invalid function description: {function_desc}")
        else:
            function_name = function_desc["name"]

        function_model = FUNCTIONS[function_name]
        function = function_model.model_validate(function_desc)
    elif isinstance(function_desc, Function):
        function = function_desc
    else:
        raise ValueError(f"Invalid function description: {function_desc}")

    return function

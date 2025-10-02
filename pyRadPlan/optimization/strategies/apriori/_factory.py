"""Factory methods to manage available a priori strategy implementations."""

import warnings
import logging
from typing import Union, Type
from ._base import APrioriStrategyBase

APRIORISTRATEGIES = {}

logger = logging.getLogger(__name__)


def register_apriori_strategy(apriori_cls: Type[APrioriStrategyBase]) -> None:
    """
    Register a new a priori strategy.

    Parameters
    ----------
    apriori_cls : type
        An A priori Strategy class.
    """
    if not issubclass(apriori_cls, APrioriStrategyBase):
        raise ValueError("A priori strategy must be a subclass of APrioriStrategyBase.")

    if apriori_cls.short_name is None:
        raise ValueError("A priori strategy must have a 'short_name' attribute.")

    if apriori_cls.name is None:
        raise ValueError("A priori strategy must have a 'name' attribute.")

    apriori_name = apriori_cls.short_name
    if apriori_name in APRIORISTRATEGIES:
        warnings.warn(f"A priori strategy '{apriori_name}' is already registered.")
    else:
        APRIORISTRATEGIES[apriori_name] = apriori_cls


def get_available_apriori_strategies() -> dict[str]:
    """
    Get a list of available a priori strategies based on the plan.

    Returns
    -------
    list
        A list of available a priori strategies.
    """
    return APRIORISTRATEGIES


def get_apriori_strategy(
    apriori_desc: Union[str, dict],
    apriori_model_params,  # TODO: Define type,
    eval_callbacks: dict,
    solver_desc: Union[str, dict],
) -> APrioriStrategyBase:
    """
    Returns an a priori strategy instance based on a descriptive parameter.

    Parameters
    ----------
    apriori_desc : Union[str, dict]
        A string with the strategy name, or a dictionary with the strategy configuration

    Returns
    -------
    APrioriStrategyBase
        A strategy instance
    """
    if isinstance(apriori_desc, str):
        strategy = APRIORISTRATEGIES[apriori_desc](
            apriori_model_params, eval_callbacks, solver_desc
        )

    elif isinstance(apriori_desc, dict):
        raise NotImplementedError(
            "A priori strategy configuration from dictionary not implemented yet."
        )
    else:
        raise ValueError(f"Invalid a priori strategy description: {apriori_desc}")

    return strategy

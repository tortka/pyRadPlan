from abc import ABC, abstractmethod
from typing import ClassVar, Union
import numpy as np
from ..apriori import APrioriStrategyBase, get_apriori_strategy


class TradeoffStrategyBase(ABC):
    """
    To be written later
    Abstract class for tradeoff exploration methods

    Parameters
    ----------

    Attributes
    ----------
    """

    short_name: ClassVar[str]
    name: ClassVar[str]
    apriori_strategy: Union[str, dict, APrioriStrategyBase]
    # apriori_model_params, #TODO: Define type
    callbacks: dict[str, callable]
    solver: Union[str, dict]

    def __init__(
        self,
        callbacks: dict[str, callable],
        apriori_desc: Union[str, dict],
        apriori_model_params,  # TODO: Define type,
        solver_desc: Union[str, dict],
    ):
        self.callbacks = callbacks
        self.apriori_strategy = apriori_desc
        self.apriori_model_params = apriori_model_params
        self.solver = solver_desc

    def solve(self, x: np.ndarray[float]) -> list[np.ndarray[float]]:
        self._initialize()
        return self._solve(x)

    def _initialize(self):
        self.apriori_strategy = get_apriori_strategy(
            self.apriori_strategy,
            self.apriori_model_params,
            self.callbacks,
            self.solver,
        )  # TODO: Pass options

    @abstractmethod
    def _solve(self, x: np.ndarray[float]) -> list[np.ndarray[float]]:
        pass

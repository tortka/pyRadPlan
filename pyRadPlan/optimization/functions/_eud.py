"""Equivalent uniform dose function."""

from typing import Annotated
from pydantic import Field

from numba import njit
from numpy import sum as npsum

from ._function import Function, ParameterMetadata


class EUD(Function):
    """
    Equivalent uniform dose (EUD) function.

    Attributes
    ----------
    k : float
        exponent.
    eud_ref : float
        reference value
    """

    name = "EUD"

    eud_ref: Annotated[float, Field(default=0.0, ge=0.0), ParameterMetadata(kind="reference")]
    k: Annotated[float, Field(default=1.0), ParameterMetadata()]

    def compute_function(self, values):
        return _compute_function(values, self.eud_ref, self.k)

    def compute_gradient(self, values):
        return _compute_gradient(values, self.eud_ref, self.k)


@njit
def _compute_function(dose, eud_ref, eud_k):
    eud = (npsum(dose ** (1 / eud_k)) / len(dose)) ** eud_k

    return (eud - eud_ref) ** 2


@njit
def _compute_gradient(dose, eud_ref, eud_k):
    eud = (npsum(dose ** (1 / eud_k)) / len(dose)) ** eud_k
    eud_gradient = (
        npsum(dose ** (1 / eud_k)) ** (eud_k - 1) * dose ** (1 / eud_k - 1) / (len(dose) ** eud_k)
    )

    return 2.0 * (eud - eud_ref) * eud_gradient

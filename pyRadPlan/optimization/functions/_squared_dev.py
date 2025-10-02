"""Squared Deviation Function."""

from typing import Annotated
from pydantic import Field

from numba import njit

from ._function import Function, ParameterMetadata

# %% Class definition


class SquaredDeviation(Function):
    """
    Squared Deviation (least-squares) function.

    Attributes
    ----------
    d_ref : float
        dose reference value
    """

    name = "Squared Deviation"

    d_ref: Annotated[float, Field(default=60.0, ge=0.0), ParameterMetadata(kind="reference")]

    def compute_function(self, values):
        return _compute_function(values, self.d_ref)

    def compute_gradient(self, values):
        return _compute_gradient(values, self.d_ref)


@njit
def _compute_function(dose, d_ref):
    deviation = dose - d_ref

    return (deviation @ deviation) / len(dose)


@njit
def _compute_gradient(dose, d_ref):
    return 2.0 * (dose - d_ref) / len(dose)

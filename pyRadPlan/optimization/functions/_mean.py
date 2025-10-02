"""Mean dose function."""

from typing import Annotated
from pydantic import Field

from numba import njit
from numpy import ones

from ._function import Function, ParameterMetadata

# %% Class definition


class MeanDose(Function):
    """
    Mean Dose function.

    Attributes
    ----------
    d_ref : float
        reference mean dose to achieve

    Notes
    -----
    While we implement a reference value, we suggest to only use 0 as reference
    """

    name = "Mean Dose"

    d_ref: Annotated[float, Field(default=0.0, ge=0.0), ParameterMetadata(kind="reference")]

    def compute_function(self, values):
        return _compute_function(values, self.d_ref)

    def compute_gradient(self, values):
        return _compute_gradient(
            values,
            self.d_ref,
        )


@njit
def _compute_function(dose, d_ref):
    return (dose.mean() - d_ref) ** 2


@njit
def _compute_gradient(dose, d_ref):
    grad = 2 * (dose.mean() - d_ref) * ones(dose.shape) / dose.size
    return grad

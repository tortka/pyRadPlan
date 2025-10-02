"""Dose uniformity function."""

from math import sqrt
from numba import njit
from numpy.typing import NDArray

from ._function import Function


class DoseUniformity(Function):
    """Uniformity (minimize standard deviation) function."""

    name = "Dose Uniformity"

    def compute_function(self, values):
        return _compute_function(values)

    def compute_gradient(self, values):
        return _compute_gradient(values)


@njit
def _compute_function(dose: NDArray):
    return sqrt(len(dose) / (len(dose) - 1)) * dose.std()


@njit
def _compute_gradient(dose: NDArray):
    grad = dose - dose.mean()
    std_val = dose.std()
    if std_val > 0.0:
        grad /= sqrt((len(dose) - 1) * len(dose)) * std_val
    else:
        grad.fill(0.0)

    return grad

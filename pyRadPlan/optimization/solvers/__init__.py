"""A module for the solvers."""

from ._base_solvers import SolverBase, NonLinearOptimizer

try:
    from ._ipyopt import IpyoptSolver
    register_solver(IpyoptSolver)

except ImportError:
    IpyoptSolver = None
    
from ._scipy import SciPySolver
from ._factory import register_solver, get_available_solvers, get_solver

register_solver(SciPySolver)


__all__ = [
    "NonLinearOptimizer",
    "IpyoptSolver",
    "SciPySolver",
    "SolverBase",
    "get_available_solvers",
    "get_solver",
    "register_solver"
	]

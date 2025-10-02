"""Base Implementation for optimization functions."""

from abc import abstractmethod
from typing import ClassVar, Any, Literal, Union, Optional
import logging

from pydantic import computed_field, Field, field_validator, model_validator

from pyRadPlan.core.datamodel import PyRadPlanBaseModel
from pyRadPlan.quantities import get_available_quantities

ParameterType = Union[Literal["reference", "numeric", "relative_volume"], list[str]]

logger = logging.getLogger(__name__)


class ParameterMetadata:
    """
    Parameter Metadata to attach to optimization function parameters to
    designate configurability and
    type.

    Parameters
    ----------
    configurable : bool, optional, default=True
        Whether the parameter is intended to be configurable (e.g. a reference dose value for
        optimization)
    kind : str, optional, default='numeric'
        Type/Meaning of the parameter. Options are 'reference' (relates to the input vector, e.g.
        the dose when you optimize on dose. Used for normalization), 'numeric', 'relative_volume'.
        The kind is used in case the parameter needs to pre transformed in context.

    Attributes
    ----------
    configurable : bool, optional, default=True
        Whether the parameter is intended to be configurable (e.g. a reference dose value for
        optimization)
    kind : str, optional, default='numeric'
        Type/Meaning of the parameter. Options are 'reference' (relates to the input vector, e.g.
        the dose when you optimize on dose. Used for normalization), 'numeric', 'relative_volume'.
        The kind is used in case the parameter needs to pre transformed in context.

    Note
    ----
    Intended for use with 'Annotated' when defining a function attribute.
    """

    configurable: bool
    kind: Optional[ParameterType]

    """Configurable Parameter."""

    def __init__(self, configurable: bool = True, kind: Optional[ParameterType] = "numeric"):
        self.configurable = configurable
        self.kind = kind

    def __repr__(self):
        return f"{self.__class__}({self.__dict__})"


class Function(PyRadPlanBaseModel):
    """
    Base class for functions in the optimization problem.

    Attributes
    ----------
    name : ClassVar[str]
        Name of the optimization function.
    has_hessian : ClassVar[bool]
        Whether the optimization function has a Hessian implementation.
    priority : float
        Weight/Priority assigned to the optimization function.
    quantity : str
        The quantity this function is connected to (e.g. 'physical_dose', 'RBExDose').
    is_linear : bool
        bool to indicate if the function is linear.
    is_convex : bool
        bool to indicate if the function is convex.
    """

    name: ClassVar[str]
    has_hessian: ClassVar[bool] = False

    is_linear: ClassVar[bool] = False
    is_convex: ClassVar[bool] = True

    priority: float = Field(default=1.0, ge=0.0, alias="penalty")
    quantity: str = Field(default="physical_dose")

    @abstractmethod
    def compute_function(self, values):
        """Computes the objective function."""

    @abstractmethod
    def compute_gradient(self, values):
        """Computes the function gradient."""

    def compute_hessian(self, values):
        """Computes the function Hessian."""
        return

    @computed_field
    @property
    def parameter_names(self) -> list[str]:
        """List[str]: Parameter names."""
        return self._parameter_names()

    @classmethod
    def _parameter_names(cls) -> list[str]:
        """List[str]: Parameter names as classmethod."""
        return [
            name
            for name, info in cls.model_fields.items()
            if any(isinstance(meta, ParameterMetadata) for meta in info.metadata)
        ]

    @computed_field
    @property
    def parameter_types(self) -> list[ParameterType]:
        """List[str]: Parameter types."""
        return self._parameter_types()

    @classmethod
    def _parameter_types(cls) -> list[ParameterType]:
        """List[str]: Parameter types as classmethod."""
        return [
            meta.kind
            for name in cls._parameter_names()
            for meta in cls.model_fields[name].metadata
            if isinstance(meta, ParameterMetadata)
        ]

    @computed_field
    @property
    def parameters(self) -> list[Any]:
        """List[str]: Parameter values."""
        return [getattr(self, name) for name in self.parameter_names]

    @field_validator("quantity")
    @classmethod
    def _validate_quantity(cls, v):
        """Validates the quantity attribute."""
        if v not in get_available_quantities():
            raise ValueError(
                f"Quantity {v} not available. Choose from {get_available_quantities()}"
            )
        return v

    @model_validator(mode="before")
    @classmethod
    def _validate_model(cls, data: Any) -> Any:
        """Pre-validate the input and perform conversions if necessary."""

        # Check if this is a matRad-like function
        if isinstance(data, dict) and "className" in data:
            data = data.copy()

            # Should we confirm once more we have the correct function?
            data.pop("className")

            params = data.get("parameters", [])

            # If there are not more than one parameter,
            # it will usually not be in a list so we put it into one
            if not isinstance(params, list):
                params = [params]

            # obtain the parameter names
            param_names = cls._parameter_names()

            if len(params) != len(param_names):
                logger.warning(
                    "Function '%s' expects %d parameters, but %d were provided.",
                    cls.name,
                    len(param_names),
                    len(params),
                )

            for param in param_names:
                data[param] = params.pop(0)

            data.pop("parameters", None)

        return data

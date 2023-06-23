from typing import Any, TypeVar, cast

from expressions.context import Context, NoDefault
from expressions.exceptions import (
    ContextVariableNotFoundError,
    VariableNotFoundError,
    VariableTypeError,
)
from expressions.expr.expr_base import Expression, ExpressionArity, MappeableMixin

T = TypeVar("T")


class Variable(Expression[T], MappeableMixin):
    """Variable expression."""

    arity = ExpressionArity.NULLARY
    params_type_map: dict[str, type] = {
        "name": str,
        "return_type": type,
        # we are explicitly adding `type[NoDefault] to highlight its importance:
        # default=NoDefault indicates no default was specified, which is different from
        # default=None
        "default": Any | type[NoDefault],  # type: ignore
    }
    sub_expression_names: tuple[str] = ()  # type: ignore

    def __init__(self, name: str, return_type: type, default: Any = NoDefault):
        """Variable expression constructor."""
        self.name = name
        self.return_type = return_type
        self.default = default

    def evaluate(self, context: Context) -> T:
        """Evalaute this expressionn in the given context, returning a value."""
        try:
            value = context.get(self.name, self.default)
        except ContextVariableNotFoundError as exc:
            raise VariableNotFoundError(f"variable {self.name!s} not found") from exc

        if not isinstance(value, self.return_type):
            raise VariableTypeError(
                f"Variable '{self.name}' has incorrect type, "
                f"expected: {self.return_type}, gotten: {type(value)}",
            )
        return value  # type: ignore

    def sub_expressions(self) -> tuple[Expression, ...]:
        """Return sub-expressions of this expression."""
        return ()

    def to_dict(self) -> dict[str, Any]:
        """Return dictionary with all parameters used to build the current instance."""
        dct = {"name": self.name, "return_type": self.return_type}
        if self.default != NoDefault:
            dct["default"] = self.default
        return dct

    def __eq__(self, other: object) -> bool:
        """Return true if expressions are equal."""
        # they must be of the same type
        if self.__class__ != other.__class__:
            return False

        other_var = cast(Variable, other)
        return (
            self.name == other_var.name
            and self.return_type == other_var.return_type
            and self.default == other_var.default
        )

    def __repr__(self) -> str:
        """String representation for this instance."""
        opt_default = f", default={self.default}" if self.default != NoDefault else ""
        return f"Variable({self.name=!r}, {self.return_type=!r}{opt_default})"

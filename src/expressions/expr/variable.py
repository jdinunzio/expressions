from typing import Any, TypeVar

from expressions.context import Context, NoDefault
from expressions.exceptions import (
    ContextVariableNotFoundException,
    VariableNotFoundException,
    VariableTypeException,
)
from expressions.expr.expr_base import Expression, ExpressionArity

T = TypeVar("T")


class Variable(Expression[T]):
    """Variable expression."""

    arity = ExpressionArity.NULLARY

    def sub_expressions(self) -> tuple[Expression, ...]:
        return ()

    def __init__(self, name: str, return_type: type, default: Any = NoDefault):
        self.name = name
        self.return_type = return_type
        self.default = default

    def evaluate(self, context: Context) -> T:
        try:
            value = context.get(self.name, self.default)
        except ContextVariableNotFoundException as exc:
            raise VariableNotFoundException(f"variable {self.name!s} not found") from exc

        if not isinstance(value, self.return_type):
            raise VariableTypeException(
                f"Variable '{self.name}' has incorrect type, "
                f"expected: {self.return_type}, gotten: {type(value)}"
            )
        return value  # type: ignore

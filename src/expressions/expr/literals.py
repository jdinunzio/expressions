from typing import Any, Generic, cast

from expressions.context import Context
from expressions.exceptions import ExpressionValidationError
from expressions.expr.expr_base import Expression, ExpressionArity, T
from expressions.expr.expr_types import BooleanExpression


class LiteralMixin(Generic[T]):
    """Mixin for all literal expressions."""

    return_type: Any
    is_literal: bool = True
    arity: ExpressionArity = ExpressionArity.NULLARY

    def __init__(self, value: T) -> None:
        """Literal constructor."""
        self._assert_valid_literal(value)
        self.value = value

    def _assert_valid_literal(self, value: Any) -> None:
        """Raise exception if literal value is of the wrong type."""
        if not isinstance(value, self.return_type):
            raise ExpressionValidationError(
                "expression validation error",
                [{"value": "literal value is not {self.return_type}"}],
            )

    def sub_expressions(self) -> tuple[Expression]:
        """Return list of direct sub-expressions of this expression."""
        return cast(tuple[Expression], ())

    def evaluate(self, _: Context) -> T:
        """Evaluate expression in context."""
        return self.value


class Boolean(LiteralMixin[bool], BooleanExpression):
    """Boolean literal expression."""

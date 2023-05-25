from typing import Any, Sequence

from expressions.context import Context
from expressions.exceptions import ExpressionValidationError
from expressions.expr.expr_base import ExpressionArity, HomogeneousListMixin
from expressions.expr.literals import (
    BooleanExpression,
    DatetimeExpression,
    NumericExpression,
    StringExpression,
    TimedeltaExpression,
)

Comparable = (
    BooleanExpression
    | NumericExpression
    | StringExpression
    | DatetimeExpression
    | TimedeltaExpression
)


class Comparison(HomogeneousListMixin[Comparable], BooleanExpression):
    """Base class for comparison expressions."""

    arity: ExpressionArity = ExpressionArity.BINARY

    def _assert_valid_sub_expressions(self, sub_exprs: Sequence[Any]) -> None:
        """Raise exception if literal value is of the wrong type."""
        if len(sub_exprs) <= 1:
            return
        expected_type = type(sub_exprs[0])
        errors: list[dict] = []
        for i, sub_expr in enumerate(sub_exprs):
            if not isinstance(sub_expr, expected_type):
                errors.append({"argument_index": i, "argument_type": str(type(sub_expr))})
        if errors:
            raise ExpressionValidationError("expression validation error", errors)


class Equal(Comparison):
    """Equal comparison expression."""

    def evaluate(self, context: Context) -> bool:
        """Evaluate not expression in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left == right


class NotEqual(Comparison):
    """Not equal comparison expression."""

    def evaluate(self, context: Context) -> bool:
        """Evaluate not equal expression in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left != right


class LessThan(Comparison):
    """Less than comparison expression."""

    def evaluate(self, context: Context) -> bool:
        """Evaluate less than expression in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left < right


class LessThanOrEqual(Comparison):
    """Less than or equal comparison expression."""

    def evaluate(self, context: Context) -> bool:
        """Evaluate less or equal expression in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left <= right


class GreaterThan(Comparison):
    """Greater than comparison expression."""

    def evaluate(self, context: Context) -> bool:
        """Evaluate greater than expression in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left > right


class GreaterThanOrEqual(Comparison):
    """Greater than or equal comparison expression."""

    def evaluate(self, context: Context) -> bool:
        """Evaluate greater or equal than expression in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left >= right

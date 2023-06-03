from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, Generic, cast

from expressions.context import Context
from expressions.exceptions import ExpressionValidationError
from expressions.expr.expr_base import Expression, ExpressionArity, T
from expressions.expr.expr_types import (
    BooleanExpression,
    DatetimeExpression,
    NumericExpression,
    StringExpression,
    TimedeltaExpression,
)


class LiteralMixin(Generic[T]):
    """Mixin for all literal expressions.

    Literal expressions represent literal values and evaluate to them. They have nullary arity,
    since don't contain any sub-expression, making them terminal expressions.
    """

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

    def __eq__(self, other: object) -> bool:
        """Return true if expressions are equal."""
        # they must be of the same type
        if self.__class__ != other.__class__:
            return False

        # and must have the same value
        return self.value == cast(LiteralMixin, other).value

    def __repr__(self) -> str:
        """Return string representation of this instance."""
        return f"{self.__class__.__name__}({self.value!s})"


class Null(LiteralMixin[None], Expression[None]):
    """Null literal expression."""

    return_type = type(None)

    def __init__(self, _=None) -> None:
        """Literal constructor."""
        super().__init__(None)


class Boolean(LiteralMixin[bool], BooleanExpression):
    """Boolean literal expression."""


class Number(LiteralMixin[Decimal], NumericExpression):
    """Numeric literal expression."""

    def __init__(self, value: bool | int | float | str | Decimal) -> None:
        """Literal constructor."""
        if not isinstance(value, int | float | str | Decimal):
            raise ExpressionValidationError(
                "expression validation error",
                [{"value": "literal value is not int, float, string or decimal"}],
            )
        try:
            # convert number to string before decimalise it to get a "better" (more rounded)
            # representation
            dec_value = Decimal(str(value))
        except InvalidOperation as exc:
            raise ExpressionValidationError(
                "expression validation error",
                [{"value": "given string cannot be converted into number"}],
            ) from exc
        super().__init__(Decimal(dec_value))


class String(LiteralMixin[str], StringExpression):
    """String literal expression."""


class Datetime(LiteralMixin[datetime], DatetimeExpression):
    """Datetime literal expression."""

    def __repr__(self) -> str:
        """Return string representation of this instance."""
        return f"{self.__class__.__name__}({self.value.isoformat()})"


class Timedelta(LiteralMixin[timedelta], TimedeltaExpression):
    """Timedelta literal expression."""

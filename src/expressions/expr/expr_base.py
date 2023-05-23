import abc
from enum import IntEnum
from typing import Any, Generic, TypeVar

from expressions.context import Context
from expressions.exceptions import ExpressionValidationError

T = TypeVar("T")


class ExpressionArity(IntEnum):
    """Expression arity enum."""

    NULLARY = 0
    UNARY = 1
    BINARY = 2
    TERNARY = 3
    N_ARY = 4


class Expression(abc.ABC, Generic[T]):
    """Base Class for all expressions."""

    return_type: type  # type(T)
    is_literal: bool
    arity: ExpressionArity

    @property
    @classmethod
    def is_terminal(cls) -> bool:
        """Return true if this expression is terminal.

        Returns:
            True if expressions of this type are terminal.
        """
        return cls.arity == ExpressionArity.NULLARY

    @abc.abstractmethod
    def evaluate(self, context: Context) -> T:
        """Evaluate expression in context.

        Args:
            context: Evaluation context.

        Returns:
            Result of evaluating the expression in the given context.

        Raises:
            ExpressionEvaluationError.
        """


class LiteralExpression(Expression[T]):
    """Base Class for all expressions."""

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

    def evaluate(self, _: Context) -> T:
        """Evaluate expression in context."""
        return self.value

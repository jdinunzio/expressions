from __future__ import annotations

import abc
from enum import IntEnum
from typing import Any, Generic, Sequence, TypeVar

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
    AT_LEAST_TWO = 12

    def has_list_right_arity(self, lst: list) -> bool:
        """Return True if the given list has length compatible with this arity."""
        arity = len(lst)
        match self:
            case ExpressionArity.NULLARY:
                return arity == 0
            case ExpressionArity.UNARY:
                return arity == 1
            case ExpressionArity.BINARY:
                return arity == 2
            case ExpressionArity.TERNARY:
                return arity == 3
            case ExpressionArity.N_ARY:
                return True
            case ExpressionArity.AT_LEAST_TWO:
                return arity >= 2


class Expression(abc.ABC, Generic[T]):
    """Base Class for all expressions."""

    return_type: type  # type(T)
    is_literal: bool = False
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
    def sub_expressions(self) -> tuple[Expression, ...]:
        """Return list of direct sub-expressions of this expression.

        Returns:
            List of sub-expressions of this expression.
        """

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


class HomogeneousListMixin(Generic[T]):
    """Mixin for expressions that contains a list of sub-expressions of the same type."""

    arity: ExpressionArity = ExpressionArity.N_ARY
    _items_type: type[Expression]
    _sub_expressions: tuple[Expression, ...]

    def __init__(self, *sub_expressions: T) -> None:
        """Constructor for expression with homogeneous list of sub-expressions."""
        self._assert_valid_sub_expressions(sub_expressions)
        self._sub_expressions = sub_expressions  # type: ignore

    def _assert_valid_sub_expressions(self, sub_exprs: Sequence[Any]) -> None:
        """Raise exception if literal value is of the wrong type."""
        errors: list[dict] = []
        for i, sub_expr in enumerate(sub_exprs):
            if not isinstance(sub_expr, self._items_type):
                errors.append({"argument_index": i, "argument_type": str(type(sub_expr))})
        if errors:
            raise ExpressionValidationError("expression validation error", errors)

    def sub_expressions(self) -> tuple[Expression, ...]:
        """Return list of direct sub-expressions of this expression."""
        return self._sub_expressions

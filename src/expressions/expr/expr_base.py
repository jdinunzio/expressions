from __future__ import annotations

import abc
from enum import IntEnum
from typing import Any, Generic, Sequence, TypeVar, cast

from expressions.context import Context
from expressions.exceptions import ExpressionValidationError

T = TypeVar("T")


class ExpressionArity(IntEnum):
    """Expression arity enum.

    Expression arity indicates how many _sub-expressions_ an expression has. Other required elements
    don't count when considering arity, so for example Literal expressions that require a literal
    value to be constructed have arity zero.
    """

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
    """Generic Class for all expressions.

    This class is generic on the type of the value the expression evaluates to.
    """

    return_type: type  # type(T)
    is_literal: bool = False
    arity: ExpressionArity

    @property
    @classmethod
    def is_terminal(cls) -> bool:
        """Return true if this expression is terminal.

        An expression is terminal if it doesn't contain any sub-expression.

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

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """Return true if expressions are equal."""


class HomogeneousListMixin(Generic[T]):
    """Mixin for expressions that contains a list of sub-expressions of the same type.

    Examples of these types of expressions are the basic arithmetic operations, and comparisons.
    """

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

    def __eq__(self, other: object) -> bool:
        """Return true if expressions are equal."""
        # they must be of the same type
        if self.__class__ != other.__class__:
            return False

        # they must have the same number of sub-expressions
        self_subs = self.sub_expressions()
        other_subs = cast(HomogeneousListMixin, other).sub_expressions()
        if len(self_subs) != len(other_subs):
            return False

        # their sub-expressions must be equal (and in the same order)
        return all((self_sub == other_sub for (self_sub, other_sub) in zip(self_subs, other_subs)))

    def __repr__(self) -> str:
        """Return string representation of this instance."""
        subs_repr = ", ".join([repr(sub) for sub in self.sub_expressions()])
        return f"{self.__class__.__name__}({subs_repr})"


class MappeableMixin:
    """Mixin for expressions that can be represented as a map from keys to values.

    The map represent all parameters that can be used to create an instance of this expression.
    Values in the map don't need to be expressions.
    """

    # This property can be use to introspect on how to create instances of this expression
    params_type_map: dict[str, type]
    # tuple with the name of the parameters that are sub-expressions
    sub_expression_names: tuple[str]

    @abc.abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Return dictionary with all parameters used to build the current instance.

        Returns:
            Dictionary with all parameters used to build the current instance.
        """

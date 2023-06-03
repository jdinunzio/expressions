from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from expressions.expr.expr_base import Expression

T = TypeVar("T")


class Parser(ABC, Generic[T]):
    """Parser interface."""

    @abstractmethod
    def serialise(self, expr: Expression) -> T:
        """Serialise an expression.

        Args:
            expr: Expression to serialise.

        Returns:
            The expression serialised.
        """

    @abstractmethod
    def parse(self, data: T) -> Expression:
        """Parse an expression representation into an expression.

        Args:
            data: Expression representation.

        Returns:
            Parsed expression.

        Raises:
            ParseException.
        """

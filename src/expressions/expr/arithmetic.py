from decimal import Decimal
from functools import reduce
from operator import mul

from expressions.context import Context
from expressions.exceptions import ExpressionEvaluationError
from expressions.expr.expr_base import ExpressionArity, HomogeneousListMixin
from expressions.expr.expr_types import NumericExpression


class Arithmetic(HomogeneousListMixin[NumericExpression], NumericExpression):
    """Base class for arithmetic expressions."""

    _items_type = NumericExpression


class Add(Arithmetic):
    """Addition expression."""

    arity = ExpressionArity.AT_LEAST_TWO

    def evaluate(self, context: Context) -> Decimal:
        """Evaluate addition in context."""
        return sum((expr.evaluate(context) for expr in self.sub_expressions()))  # type: ignore


class Sub(Arithmetic):
    """Subtraction expression."""

    arity = ExpressionArity.BINARY

    def evaluate(self, context: Context) -> Decimal:
        """Evaluate subtraction in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left - right


class Mul(Arithmetic):
    """Multiplication expression."""

    arity = ExpressionArity.AT_LEAST_TWO

    def evaluate(self, context: Context) -> Decimal:
        """Evaluate multiplication in context."""

        return reduce(mul, (expr.evaluate(context) for expr in self._sub_expressions), Decimal(1))


class Div(Arithmetic):
    """Division expression."""

    arity = ExpressionArity.BINARY

    def evaluate(self, context: Context) -> Decimal:
        """Evaluate division in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        if right == 0:
            raise ExpressionEvaluationError("division by zero")
        return left / right


class Mod(Arithmetic):
    """Module expression."""

    arity = ExpressionArity.BINARY

    def evaluate(self, context: Context) -> Decimal:
        """Evaluate modulo in context."""
        left = self._sub_expressions[0].evaluate(context)
        right = self._sub_expressions[1].evaluate(context)
        return left % right

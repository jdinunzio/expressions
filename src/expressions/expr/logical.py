from expressions.context import Context
from expressions.expr.expr_base import ExpressionArity, HomogeneousListMixin
from expressions.expr.expr_types import BooleanExpression


class Logical(HomogeneousListMixin[BooleanExpression], BooleanExpression):
    """Base class for comparison expressions."""

    _items_type = BooleanExpression


class Not(Logical):
    """Logical Not Expression."""

    arity = ExpressionArity.UNARY

    def evaluate(self, context: Context) -> bool:
        """Evaluate not expression in context."""
        return not self._sub_expressions[0].evaluate(context)


class And(Logical):
    """Logical And Expression."""

    arity = ExpressionArity.N_ARY

    def evaluate(self, context: Context) -> bool:
        """Evaluate and expression lazily in context."""
        for sub_expr in self._sub_expressions:
            if not sub_expr.evaluate(context):
                return False
        return True


class Or(Logical):
    """Logical Or Expression."""

    arity = ExpressionArity.N_ARY

    def evaluate(self, context: Context) -> bool:
        """Evaluate and expression lazily in context."""
        for sub_expr in self._sub_expressions:
            if sub_expr.evaluate(context):
                return True
        return False

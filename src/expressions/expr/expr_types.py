from __future__ import annotations

from expressions.expr.expr_base import Expression


class BooleanExpression(Expression[bool]):
    """Base class for all boolean expressions."""

    return_type = bool

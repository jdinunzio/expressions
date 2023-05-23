from expressions.expr.expr_base import LiteralExpression


class Boolean(LiteralExpression[bool]):
    """Boolean literal expression."""

    return_type = bool

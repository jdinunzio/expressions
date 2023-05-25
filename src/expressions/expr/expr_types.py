from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

from expressions.expr.expr_base import Expression


class BooleanExpression(Expression[bool]):
    """Base class for all boolean expressions."""

    return_type = bool


class NumericExpression(Expression[Decimal]):
    """Base class for all numeric expressions."""

    return_type = Decimal


class StringExpression(Expression[str]):
    """Base class for all string expressions."""

    return_type = str


class DatetimeExpression(Expression[datetime]):
    """Base class for all datetime expressions."""

    return_type = datetime


class TimedeltaExpression(Expression[timedelta]):
    """Base class for all boolean expressions."""

    return_type = timedelta

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any
from unittest import TestCase

import pytz

from expressions import Expression
from expressions.exceptions import ExpressionValidationError
from expressions.expr.literals import Boolean, Datetime, Null, Number, String, Timedelta


class BaseLiteralMixin:  # pylint: disable=no-member
    """Base class for all literal tests."""

    literal_type: type[Expression]
    valid_literals: tuple[Any, ...]
    invalid_literals: tuple[Any, ...] = (
        None,
        False,
        True,
        0,
        -3,
        2.5,
        Decimal(3.3),
        "hello",
        datetime.now(tz=pytz.utc),
        timedelta(hours=1),
    )

    def test_is_literal(self):
        """Literal expression are identified as literals."""
        for val in self.valid_literals:
            with self.subTest(val):
                expr = self.literal_type(val)
                self.assertTrue(expr.is_literal)

    def test_return_type_is_right(self):
        """Literal expression has the return type of their literals."""
        val = self.valid_literals[0]
        expr = self.literal_type(val)
        self.assertEqual(expr.return_type, type(val))

    def test_literal_evaluates_to_value(self):
        """Literal expression evaluate to its literal value."""
        for val in self.valid_literals:
            with self.subTest(val):
                expr = self.literal_type(val)
                self.assertEqual(expr.evaluate({}), val)

    def test_raises_on_invalid_params(self):
        """Literal expression should raise if created with invalid parameters."""
        for val in self.invalid_literals:
            if isinstance(val, self.literal_type.return_type):
                continue

            with self.subTest(val):
                with self.assertRaises(ExpressionValidationError):
                    self.literal_type(val)


class TestNullLiteral(TestCase):
    """Test case for null literals."""

    literal_type = Null
    valid_literals = (None,)

    def test_is_literal(self):
        """Literal expression are identified as literals."""
        expr = Null()
        self.assertTrue(expr.is_literal)

    def test_return_type_is_right(self):
        """Literal expression has the return type of their literals."""
        expr = Null()
        self.assertEqual(expr.return_type, type(None))

    def test_literal_evaluates_to_value(self):
        """Literal expression evaluate to its literal value."""
        expr = Null()
        self.assertIsNone(expr.evaluate({}))


class TestBooleanLiteral(TestCase, BaseLiteralMixin):
    """Test case for boolean literals."""

    literal_type = Boolean
    valid_literals = (False, True)


class TestNumberLiteral(TestCase, BaseLiteralMixin):
    """Test case for number literals."""

    literal_type = Number
    valid_literals = (-3, 0, 1.1, Decimal(2.3))
    invalid_literals = (
        None,
        "hello",
        datetime.now(tz=pytz.utc),
        timedelta(hours=1),
    )

    def test_return_type_is_right(self):
        """Literal expression has the return type of their literals."""
        val = self.valid_literals[0]
        expr = self.literal_type(val)
        self.assertEqual(expr.return_type, Decimal)

    def test_literal_evaluates_to_value(self):
        """Literal expression evaluate to its literal value."""
        for val in self.valid_literals:
            with self.subTest(val):
                expr = self.literal_type(val)
                self.assertEqual(expr.evaluate({}), Decimal(val))


class TestStringLiteral(TestCase, BaseLiteralMixin):
    """Test case for string literals."""

    literal_type = String
    valid_literals = ("hello",)


class TestDatetimeLiteral(TestCase, BaseLiteralMixin):
    """Test case for datetime literals."""

    literal_type = Datetime
    valid_literals = (datetime.now(tz=pytz.utc),)


class TestTimedeltaLiteral(TestCase, BaseLiteralMixin):
    """Test case for time delta literals."""

    literal_type = Timedelta
    valid_literals = (timedelta(hours=2),)

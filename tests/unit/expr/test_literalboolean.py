from unittest import TestCase

from expressions.exceptions import ExpressionValidationError
from expressions.expr.literalboolean import Boolean


class TestBoolean(TestCase):
    """Test case for boolean expressions."""

    def test_is_literal(self):
        """Boolean literals are literal expressions."""
        for val in (True, False):
            with self.subTest(val):
                expr = Boolean(val)
                self.assertTrue(expr.is_literal)

    def test_return_type_is_right(self):
        """Boolean literal has the right return type."""
        for val in (True, False):
            with self.subTest(val):
                expr = Boolean(val)
                self.assertEqual(expr.return_type, bool)

    def test_raises_on_invalid_params(self):
        """Boolean literal should raise if created with invalid parameters."""
        for val in (None, 1, -2.2, "hi"):
            with self.subTest(val):
                with self.assertRaises(ExpressionValidationError):
                    Boolean(val)

    def test_evaluates_ok(self):
        """Boolean literals evaluate to its literal value."""
        for val in (True, False):
            with self.subTest(val):
                expr = Boolean(val)
                self.assertEqual(expr.evaluate({}), val)

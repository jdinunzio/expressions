from unittest import TestCase

from expressions import And, Boolean, Not, Or
from expressions.expr.expr_base import Expression


class BaseLogicalTest:  # pylint: disable=no-member
    """Base class for all logical tests."""

    expr_class: type[Expression]
    instance: Expression
    evaluation_cases: list[tuple[tuple, bool]]

    def test_return_type_is_right(self):
        """Logical operations have the right return type."""
        self.assertEqual(self.instance.return_type, bool)

    def test_evaluates_ok(self):
        """Logical operation evaluate to rigth result."""
        for vals, result in self.evaluation_cases:
            with self.subTest(vals):
                expr = self.expr_class(*vals)
                self.assertEqual(expr.evaluate({}), result)


class TestNot(TestCase, BaseLogicalTest):
    """Test case for Not Expression."""

    expr_class = Not
    instance = Not(Boolean(True))
    evaluation_cases = [
        ((Boolean(False),), True),
        ((Boolean(True),), False),
    ]


class TestAnd(TestCase, BaseLogicalTest):
    """Test case for And Expression."""

    expr_class = And
    instance = And(Boolean(True), Boolean(False))
    evaluation_cases = [
        ((Boolean(False), Boolean(False)), False),
        ((Boolean(False), Boolean(True)), False),
        ((Boolean(True), Boolean(False)), False),
        ((Boolean(True), Boolean(True)), True),
    ]


class TestOr(TestCase, BaseLogicalTest):
    """Test case for Or Expression."""

    expr_class = Or
    instance = Or(Boolean(True), Boolean(False))
    evaluation_cases = [
        ((Boolean(False), Boolean(False)), False),
        ((Boolean(False), Boolean(True)), True),
        ((Boolean(True), Boolean(False)), True),
        ((Boolean(True), Boolean(True)), True),
    ]

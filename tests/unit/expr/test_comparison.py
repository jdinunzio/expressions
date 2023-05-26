# pylint: disable=abstract-class-instantiated
from datetime import datetime, timedelta
from itertools import product
from operator import eq, ge, gt, le, lt, ne
from unittest import TestCase

from expressions import (
    Boolean,
    Datetime,
    Equal,
    Expression,
    GreaterThan,
    GreaterThanOrEqual,
    LessThan,
    LessThanOrEqual,
    NotEqual,
    Number,
    String,
    Timedelta,
)

V = bool | int | float | str | datetime | timedelta


class TestComparison(TestCase):
    """Comparison tests."""

    test_map: dict[type[Expression], tuple[V, V]] = {
        Boolean: (False, True),
        Number: (-3.5, 7),
        String: ("bar", "foo"),
        Datetime: (datetime(2020, 10, 12), datetime(2021, 1, 2)),
        Timedelta: (timedelta(minutes=3), timedelta(hours=2)),
    }
    compare_expressions = (
        (Equal, eq),
        (NotEqual, ne),
        (LessThan, lt),
        (LessThanOrEqual, le),
        (GreaterThan, gt),
        (GreaterThanOrEqual, ge),
    )

    def test_return_type_is_right(self):
        """Comparison operations have the right return type."""
        for compare_class, _ in self.compare_expressions:
            with self.subTest(str(compare_class)):
                for expr_class, (left_val, right_val) in self.test_map.items():
                    left = expr_class(left_val)
                    right = expr_class(right_val)
                    compare = compare_class(left, right)
                    self.assertEqual(compare.return_type, bool)

    def test_evaluates_ok(self):
        """Comparison operation evaluate to right result."""
        for compare_class, operator in self.compare_expressions:
            for expr_class, vals in self.test_map.items():
                for left_val, right_val in product(vals, vals):
                    with self.subTest(compare_class, left=left_val, right=right_val):
                        left = expr_class(left_val)
                        right = expr_class(right_val)
                        compare = compare_class(left, right)
                        self.assertEqual(compare.evaluate({}), operator(left_val, right_val))

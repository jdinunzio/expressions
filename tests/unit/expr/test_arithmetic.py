from decimal import Decimal
from unittest import TestCase

from expressions import Add, Arithmetic, Div, Mod, Mul, Number, Sub
from expressions.exceptions import ExpressionEvaluationError


class TestArithmetic(TestCase):
    """Test Arithmetic Expressions."""

    # TODO: unhappy cases: wrong number of params.

    ok_map: dict[type[Arithmetic], list[tuple[tuple, float]]] = {
        Add: [
            ((0, 1), 1),
            ((2.2, 0), 2.2),
            ((5, 4.5, -1.3), 8.2),
            ((0, 1), 1),
        ],
        Sub: [
            ((3.2, 0), 3.2),
            ((10, 2.5), 7.5),
        ],
        Mul: [((1, 2), 2), ((2, 1.0), 2.0), ((1, 2.0, 3), 6.0)],
        Div: [
            ((7.5, 1), 7.5),
            ((15, 3.0), 5.0),
        ],
        Mod: [
            ((5, 5.0), 0),
            ((7.0, 4), 3.0),
        ],
    }

    def test_return_type_is_right(self):
        """Arithmetic operations have the right return type."""
        for expr_class, cases in self.ok_map.items():
            args, _ = cases[0]
            with self.subTest(expr_class):
                expr_args = [Number(x) for x in args]
                expr = expr_class(*expr_args)
                self.assertEqual(expr.return_type, Decimal)

    def test_evaluates_ok(self):
        """Arithmetic operation evaluate to right result."""
        for expr_class, cases in self.ok_map.items():
            for args, result in cases:
                with self.subTest(expr_class.__name__, args=args, result=result):
                    expr_args = [Number(x) for x in args]
                    expr = expr_class(*expr_args)
                    self.assertAlmostEqual(expr.evaluate({}), Decimal(result))

    def test_division_by_zero_raises(self):
        """Division by zero should raise ExpressionEvaluationError."""
        expr = Div(Number(1), Number(0))
        with self.assertRaises(ExpressionEvaluationError):
            expr.evaluate({})

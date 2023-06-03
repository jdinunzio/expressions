# pylint: disable=abstract-class-instantiated
from datetime import datetime, timedelta
from decimal import Decimal
from unittest import TestCase

from expressions import (
    Add,
    And,
    Boolean,
    Datetime,
    Div,
    Equal,
    Expression,
    GreaterThan,
    GreaterThanOrEqual,
    LessThan,
    LessThanOrEqual,
    Mod,
    Mul,
    Not,
    NotEqual,
    Null,
    Number,
    Or,
    String,
    Sub,
    Timedelta,
    Variable,
)
from expressions.parser import DictParser, JsonParser, Parser
from expressions.serialiser.dict_serialiser import LiteralPrimitive


class TestPaserMixin:
    """Test case for Expression parser."""

    expr_dct: list[tuple[Expression, LiteralPrimitive]] = [
        # (expression, dict)
    ]
    parser: Parser

    def test_parse_and_serialise_is_identity(self):
        """parse() followed with serialise() should be equivalent to identity.

        Given a serialised version of an expression
        When the expression is parsed and serialised
        Then it should produce the same initial value.
        """
        for _, dct in self.expr_dct:
            with self.subTest(dct):
                self.assertEqual(self.parser.serialise(self.parser.parse(dct)), dct)

    def test_serialise_and_parse_is_identity(self):
        """serialise() followed with parse() should be equivalent to identity.

        Given an expression
        When the expression is serialised and parsed
        Then it should produce the same initial value.
        """
        for expr, _ in self.expr_dct:
            with self.subTest(expr):
                self.assertEqual(self.parser.parse(self.parser.serialise(expr)), expr)

    def test_expression_is_serialised(self):
        """serialise() should serialise an expression.

        Given an expression and a parser
        Then the parser should be able to serialise the expression.
        """
        for expr, dct in self.expr_dct:
            with self.subTest(expr):
                self.assertEqual(self.parser.serialise(expr), dct)

    def test_data_is_parseable(self):
        """parse() should generate expressions from valid serialised data.

        Given a valid serialised representation of an expression
        Then the parser should be able to parse it.
        """
        for expr, dct in self.expr_dct:
            with self.subTest(dct):
                self.assertEqual(self.parser.parse(dct), expr)


class TestDictPaser(TestPaserMixin, TestCase):
    """Test case for Dict Parser."""

    expr_dct: list[tuple[Expression, LiteralPrimitive]] = [
        # (expression, dict)
        # literals
        (Null(), None),
        (Boolean(True), True),
        (Boolean(False), False),
        (Number("1.3"), Decimal("1.3")),
        (String("Hello"), "Hello"),
        (Datetime(datetime(2020, 11, 30)), datetime(2020, 11, 30)),
        (Timedelta(timedelta(hours=3)), timedelta(hours=3)),
        # logical
        (Not(Boolean(True)), {"not": [True]}),
        (And(Boolean(True), Boolean(False)), {"and": [True, False]}),
        (Or(Boolean(False), Boolean(True)), {"or": [False, True]}),
        # comparison
        (Equal(Boolean(True), Boolean(False)), {"equal": [True, False]}),
        (NotEqual(String("hi"), String("hello")), {"not-equal": ["hi", "hello"]}),
        (GreaterThan(Number(3), Number(2)), {"greater-than": [Decimal(3), Decimal(2)]}),
        (
            GreaterThanOrEqual(Datetime(datetime(2020, 1, 2)), Datetime(datetime(2021, 2, 3))),
            {"greater-than-or-equal": [datetime(2020, 1, 2), datetime(2021, 2, 3)]},
        ),
        (
            LessThan(Timedelta(timedelta(hours=2)), Timedelta(timedelta(minutes=3))),
            {"less-than": [timedelta(hours=2), timedelta(minutes=3)]},
        ),
        (LessThanOrEqual(Number(4), Number(5)), {"less-than-or-equal": [Decimal(4), Decimal(5)]}),
        # arithmetic
        (Add(Number(2), Number(3)), {"add": [Decimal(2), Decimal(3)]}),
        (Sub(Number(2), Number(3)), {"sub": [Decimal(2), Decimal(3)]}),
        (Mul(Number(2), Number(3)), {"mul": [Decimal(2), Decimal(3)]}),
        (Div(Number(2), Number(3)), {"div": [Decimal(2), Decimal(3)]}),
        (Mod(Number(2), Number(3)), {"mod": [Decimal(2), Decimal(3)]}),
        # variable
        (Variable("x", int), {"var": {"name": "x", "return_type": int}}),
        (Variable("x", int, 3), {"var": {"name": "x", "return_type": int, "default": 3}}),
    ]
    parser: Parser = DictParser()


def obj_to_json(val: datetime | timedelta | Decimal | float | int | type) -> str:
    """Convert value into dictionary representation and then into json string."""
    if isinstance(val, datetime):
        return f'{{"__class__": "datetime", "__value__": "{val.isoformat()}"}}'
    if isinstance(val, timedelta):
        return f'{{"__class__": "timedelta", "__value__": {val.total_seconds()}}}'
    if isinstance(val, (Decimal, float, int)):
        return f'{{"__class__": "bignum", "__value__": "{val}"}}'
    if isinstance(val, type):
        return f'{{"__class__": "type", "__value__": "{val.__name__}"}}'
    # this should never occur, added to make linter happy
    raise RuntimeError(f"value {val} with type {type(val)} not allowed")


class TestJsonPaser(TestPaserMixin, TestCase):
    """Test case for Dict Parser."""

    expr_dct: list[tuple[Expression, LiteralPrimitive]] = [
        # # (expression, dict)
        # literals
        (Null(), "null"),
        (Boolean(True), "true"),
        (Boolean(False), "false"),
        (Number("1.3"), "1.3"),
        (
            Number("123456789012345678901234567890.123"),
            obj_to_json(Decimal("123456789012345678901234567890.123")),
        ),
        (String("Hello"), '"Hello"'),
        (Datetime(datetime(2020, 11, 30)), obj_to_json(datetime(2020, 11, 30))),
        (Timedelta(timedelta(hours=3)), obj_to_json(timedelta(hours=3))),
        # logical
        (Not(Boolean(True)), '{"not": [true]}'),
        (And(Boolean(True), Boolean(False)), '{"and": [true, false]}'),
        (Or(Boolean(False), Boolean(True)), '{"or": [false, true]}'),
        # # comparison
        (Equal(Boolean(True), Boolean(False)), '{"equal": [true, false]}'),
        (NotEqual(String("hi"), String("hello")), '{"not-equal": ["hi", "hello"]}'),
        (GreaterThan(Number(3), Number(2)), '{"greater-than": [3, 2]}'),
        (
            GreaterThanOrEqual(Datetime(datetime(2020, 1, 2)), Datetime(datetime(2021, 2, 3))),
            f'{{"greater-than-or-equal": [{obj_to_json(datetime(2020, 1, 2))}, '
            f"{obj_to_json(datetime(2021, 2, 3))}]}}",
        ),
        (
            LessThan(Timedelta(timedelta(hours=2)), Timedelta(timedelta(minutes=3))),
            f'{{"less-than": [{obj_to_json(timedelta(hours=2))}, '
            f"{obj_to_json(timedelta(minutes=3))}]}}",
        ),
        (LessThanOrEqual(Number(4), Number(5)), '{"less-than-or-equal": [4, 5]}'),
        # arithmetic
        (Add(Number(2), Number(3)), '{"add": [2, 3]}'),
        (Sub(Number(2), Number(3)), '{"sub": [2, 3]}'),
        (Mul(Number(2), Number(3)), '{"mul": [2, 3]}'),
        (Div(Number(2), Number(3)), '{"div": [2, 3]}'),
        (Mod(Number(2), Number(3)), '{"mod": [2, 3]}'),
        # variable
        (Variable("x", int), f'{{"var": {{"name": "x", "return_type": {obj_to_json(int)}}}}}'),
        (
            Variable("x", int, 3),
            f'{{"var": {{"name": "x", "return_type": {obj_to_json(int)}, "default": 3}}}}',
        ),
    ]
    parser: Parser = JsonParser()

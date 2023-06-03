# import dict_serialiser_init to initialise all expr<->dict serialisers and deserialisers
import expressions.serialiser.dict_serialiser_init  # noqa: F401  # pylint: disable=unused-import
from expressions.expr.expr_base import Expression
from expressions.parser.parser import Parser
from expressions.serialiser.dict_serialiser import (
    LiteralPrimitive,
    deserialiser_from_instance,
    serialiser_from_instance,
)


class DictParser(Parser[LiteralPrimitive]):
    """Parser from and to python literal primitive data types."""

    def serialise(self, expr: Expression) -> LiteralPrimitive:
        """Serialise an expression into python literal data types.

        Args:
            expr: Expression to serialise.

        Returns:
            The expression serialised.
        """
        serialiser = serialiser_from_instance(expr)
        data = serialiser.serialise(expr)  # type: ignore
        return data

    def parse(self, data: LiteralPrimitive) -> Expression:
        """Parse python literal data into an expression.

        Args:
            data: Expression representation.

        Returns:
            Parsed expression.

        Raises:
            ParseException.
        """
        deserialiser = deserialiser_from_instance(data)
        expr = deserialiser.deserialise(data)  # type: ignore
        return expr

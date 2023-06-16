# import dict_serialiser_init to initialise all expr<->dict serialisers and deserialisers
import expressions.serialiser.dict_serialiser_init  # noqa: F401  # pylint: disable=unused-import
from expressions.expr.expr_base import Expression
from expressions.parser.parser import Parser
from expressions.serialiser.dict_serialiser import (
    PrimitiveType,
    deserialiser_from_instance,
    serialiser_from_instance,
)


class PrimitiveParser(Parser[PrimitiveType]):
    """Parser from and to python literal primitive data types."""

    def serialise(self, expr: Expression) -> PrimitiveType:
        """Serialise an expression into python primitive types.

        Args:
            expr: Expression to serialise.

        Returns:
            The expression serialised into primitive python objects.
        """
        serialiser = serialiser_from_instance(expr)
        data = serialiser.serialise(expr)  # type: ignore
        return data

    def parse(self, data: PrimitiveType) -> Expression:
        """Parse python primitive data into an expression.

        Args:
            data: Expression representation in primitive python objects.

        Returns:
            Parsed expression.

        Raises:
            ParseException.
        """
        deserialiser = deserialiser_from_instance(data)
        expr = deserialiser.deserialise(data)  # type: ignore
        return expr

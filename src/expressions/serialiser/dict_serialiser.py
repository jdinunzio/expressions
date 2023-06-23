from datetime import datetime, timedelta
from decimal import Decimal
from typing import cast

import zope.interface  # type: ignore
from zope.component import getUtility  # type: ignore

from expressions import Expression
from expressions.exceptions import ParseException
from expressions.expr.expr_base import HomogeneousListMixin, MappeableMixin
from expressions.expr.literals import LiteralMixin

PrimitiveType = None | bool | int | float | Decimal | str | datetime | timedelta | dict


class IPrimitiveSerialiser(zope.interface.Interface):  # pylint: disable=inherit-non-class
    """Interface for Serialiser from Expressions to Python Primitive types."""

    def serialise(expr: Expression) -> PrimitiveType:  # pylint: disable=no-self-argument
        """Serialise expression into primitive python types."""


class IPrimitiveDeserialiser(zope.interface.Interface):  # pylint: disable=inherit-non-class
    """Interfcace fod Deserialiser from Python Primitive types to Expressions."""

    def deserialise(  # type: ignore # pylint: disable=no-self-argument
        data: PrimitiveType,
    ) -> Expression:
        """Deserialise expression from primitive python types."""


def serialiser_from_instance(expr: Expression) -> IPrimitiveSerialiser:
    """Return the dict serialiser for the given expression.

    The appropriate serialiser is a named zope adapter looked up from Zope Component Architecture
    using the expression class name.

    Args:
        expr: Expression to serialiser.

    Returns:
        Expression Serialiser.
    """
    serialiser = getUtility(IPrimitiveSerialiser, expr.__class__.__name__)
    return serialiser


def deserialiser_from_instance(data: PrimitiveType) -> IPrimitiveDeserialiser:
    """Return the dict deserialiser for the given primitive.

    The appropriate deserialiser is a named zope adapter looked up from Zope Component Architecture,
    where the name is determined by:

    * If the primitive value is a dictionary, it must have a single key which is used to select
      the appropriate adapter.
    * In other case, the deserialiser is picked from the class name of the deserialised value.

    Args:
        data: Data to deserialise.

    Returns:
        Data Deserialiser.
    """
    if isinstance(data, dict):
        # dict deserialiser is chosen by the name of its (only) key
        keys = list(data.keys())
        if len(keys) != 1:
            raise ParseException("expression {data} has more than one key")
        deserialiser_name = keys.pop()
    else:
        # other deserialisers are chosen by their class name
        deserialiser_name = data.__class__.__name__
    deserialiser = getUtility(IPrimitiveDeserialiser, deserialiser_name)
    return deserialiser


@zope.interface.implementer(IPrimitiveSerialiser)
class LiteralDictSerialiser:
    """Serialiser for literal expressions.

    Literal expressions are serialised to primitive python values by returning their value.
    """

    @staticmethod
    def serialise(expr: Expression) -> PrimitiveType:
        """Serialise literal expression."""
        return cast(LiteralMixin, expr).value


@zope.interface.implementer(IPrimitiveDeserialiser)
class LiteralDictDeserialiser:
    """Deserialiser for literal expressions.

    Instances of this class have an associated expression class. Primitive python values are
    deserialised by invoking the expression class with the primitive value.
    """

    def __init__(self, expr_class: type[LiteralMixin]) -> None:
        """Literal dictionary constructor."""
        self.expr_class = expr_class

    def deserialise(self, data: PrimitiveType) -> Expression:
        """Deserialise literal expression."""
        return cast(Expression, self.expr_class(data))


@zope.interface.implementer(IPrimitiveSerialiser)
class HomogeneousListDictSerialiser:
    """Serialiser for expressions with homogeneous lists.

    Instances of this class have an associated expression name. Homogeneous List expressions are
    serialised by returning a dictionary with a single key, the expression name, and as value the
    list of the serialised sub-expressions.
    """

    def __init__(self, expr_name: str) -> None:
        """Serialiser for expressions with homogeneous list constructor."""
        self.expr_name = expr_name

    def serialise(self, expr: Expression) -> PrimitiveType:
        """Serialise expression with homogeneous lists."""
        serialised_sub_expressions = []
        for sub_expression in expr.sub_expressions():
            serialiser = serialiser_from_instance(sub_expression)
            serialised_sub_expression = serialiser.serialise(sub_expression)  # type: ignore
            serialised_sub_expressions.append(serialised_sub_expression)
        return {self.expr_name: serialised_sub_expressions}


@zope.interface.implementer(IPrimitiveDeserialiser)
class HomogeneousListDictDeserialiser:
    """Deserialiser for expressions with homogeneous lists.

    Instances of this class have an associated expression class. Homogeneous List expressions
    serialised representation is a dictionary with a single key and as a value a list of
    serialised sub-expressions. They are deserialised by deserialising all sub-expressions in the
    list and then invoking the associated expression class with the list of deserialised
    sub-expressions.
    """

    def __init__(self, expr_class: type[HomogeneousListMixin]) -> None:
        """Deserialiser for expressions with homogeneous list constructor."""
        self.expr_class = expr_class

    def deserialise(self, data: PrimitiveType) -> Expression:
        """Deserialise expression with homogeneous lists."""
        # get the list from the first and only key in the data
        assert isinstance(data, dict)
        data_key = list(data.keys()).pop()
        data_list = data[data_key]
        sub_expressions = []
        for sub_data in data_list:
            deserialiser = deserialiser_from_instance(sub_data)
            sub_expression = deserialiser.deserialise(sub_data)  # type: ignore
            sub_expressions.append(sub_expression)
        return cast(Expression, self.expr_class(*sub_expressions))


@zope.interface.implementer(IPrimitiveSerialiser)
class MappeableSerialiser:
    """Serialiser for mappeable expressions.

    Instances of this class have an associated expression name. Mappeable expressions are
    serialised by returning a dictionary with a single key, the expression name, and as value the
    dictionary returned by the mappeable expression on which all sub-expressions have been mapped.
    """

    def __init__(self, expr_name: str) -> None:
        """Serialiser for mappeable expressions constructor."""
        self.expr_name = expr_name

    def serialise(self, expr: Expression) -> PrimitiveType:
        """Serialise mappeable expression with homogeneous lists."""
        vals_map = cast(MappeableMixin, expr).to_dict()
        for key in cast(MappeableMixin, expr).sub_expression_names:
            sub_expr = vals_map[key]
            serialiser = serialiser_from_instance(sub_expr)
            serialised_sub_expression = serialiser.serialise(sub_expr)  # type: ignore
            vals_map[key] = serialised_sub_expression
        return {self.expr_name: vals_map}


@zope.interface.implementer(IPrimitiveDeserialiser)
class MappeableDeserialiser:
    """Deserialiser for mappeable expressions.

    Instances of this class have an associated expression class. Mappeable expressions serialised
    representation is a dictionary with a single key and as a value a dictionary of serialised
    sub-expressions and other values. They are deserialised by deserialising all sub-expressions in
    the dictionary and then invoking the associated expression class with the dictionary as keyword
    arguments.
    """

    def __init__(self, expr_class: type[MappeableMixin]) -> None:
        """Deserialiser for mapped expressions constructor."""
        self.expr_class = expr_class

    def deserialise(self, data: PrimitiveType) -> Expression:
        """Deserialise mapped expression."""
        # get the list from the first and only key in the data
        assert isinstance(data, dict)
        data_key = list(data.keys()).pop()
        data_dict = data[data_key]
        # deserialise values is dict that correspond with sub-expressions
        for key in self.expr_class.sub_expression_names:
            sub_data = data_dict[key]
            deserialiser = deserialiser_from_instance(sub_data)
            sub_expression = deserialiser.deserialise(sub_data)  # type: ignore
            data_dict[key] = sub_expression
        return cast(Expression, self.expr_class(**data_dict))

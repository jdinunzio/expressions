from zope.component import provideUtility  # type: ignore

from expressions import (
    Add,
    And,
    Div,
    Equal,
    GreaterThan,
    GreaterThanOrEqual,
    LessThan,
    LessThanOrEqual,
    Mod,
    Mul,
    Not,
    NotEqual,
    Or,
    Sub,
    Variable,
)
from expressions.expr.expr_base import HomogeneousListMixin, MappeableMixin
from expressions.expr.literals import (
    Boolean,
    Datetime,
    LiteralMixin,
    Null,
    Number,
    String,
    Timedelta,
)
from expressions.serialiser.dict_serialiser import (
    HomogeneousListDictDeserialiser,
    HomogeneousListDictSerialiser,
    IPrimitiveDeserialiser,
    IPrimitiveSerialiser,
    LiteralDictDeserialiser,
    LiteralDictSerialiser,
    MappeableDeserialiser,
    MappeableSerialiser,
)


def _register_literal(klass: type[LiteralMixin], primitive_type_names: str | list[str]) -> None:
    """Register serialiser and deserialiser for Literal Expressions.

    Literal serialisers are registered with the name of the expression.
    Literal deserialisers are registered with the name of the primitive type ("bool", "str", etc.).
    """
    provideUtility(LiteralDictSerialiser, IPrimitiveSerialiser, klass.__name__)
    if not isinstance(primitive_type_names, list):
        primitive_type_names = [primitive_type_names]
    for name in primitive_type_names:
        provideUtility(LiteralDictDeserialiser(klass), IPrimitiveDeserialiser, name)


def _register_hom_list(klass: type[HomogeneousListMixin], name: str) -> None:
    """Register serialiser and deserialiser for HomogeneousListExpressions.

    Serialisers are registered with the name of the expression.
    Deserialisers are registered with the given name.
    """
    provideUtility(HomogeneousListDictSerialiser(name), IPrimitiveSerialiser, klass.__name__)
    provideUtility(HomogeneousListDictDeserialiser(klass), IPrimitiveDeserialiser, name)


def _register_mappeable(klass: type[MappeableMixin], name: str) -> None:
    """Register serialiser and deserialiser for Mappeable Expressions.

    Serialisers are registered with the name of the expression.
    Deserialisers are registered with the given name.
    """
    provideUtility(MappeableSerialiser(name), IPrimitiveSerialiser, klass.__name__)
    provideUtility(MappeableDeserialiser(klass), IPrimitiveDeserialiser, name)


def register_dict_serialisers_and_deserialisers() -> None:
    """Register serialisers and deserialisers used by dict parser.

    Serialisers and deserialisers are register using zope component architecture, like named
    utilities for IDictSerialiser and IDictDeserialiser respectively.
    """
    # literals
    _register_literal(Null, "NoneType")
    _register_literal(Boolean, "bool")
    _register_literal(Number, ["int", "float", "Decimal"])
    _register_literal(String, "str")
    _register_literal(Datetime, "datetime")
    _register_literal(Timedelta, "timedelta")
    # logical
    _register_hom_list(Not, "not")
    _register_hom_list(And, "and")
    _register_hom_list(Or, "or")
    # comparison
    _register_hom_list(Equal, "equal")
    _register_hom_list(NotEqual, "not-equal")
    _register_hom_list(LessThan, "less-than")
    _register_hom_list(LessThanOrEqual, "less-than-or-equal")
    _register_hom_list(GreaterThan, "greater-than")
    _register_hom_list(GreaterThanOrEqual, "greater-than-or-equal")
    # arithmetic
    _register_hom_list(Add, "add")
    _register_hom_list(Sub, "sub")
    _register_hom_list(Mul, "mul")
    _register_hom_list(Div, "div")
    _register_hom_list(Mod, "mod")
    # variable
    _register_mappeable(Variable, "var")


# we need to register serialisers and deserialisers on module load
register_dict_serialisers_and_deserialisers()

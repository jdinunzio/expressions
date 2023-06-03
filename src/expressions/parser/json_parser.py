import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from expressions import Expression
from expressions.parser.dict_parser import DictParser
from expressions.parser.parser import Parser

JsonPrimitive = None | bool | int | float | Decimal | str | dict


class JsonParser(Parser[str]):
    """Parser from and to json.

    It uses IDictParser to convert between expressions and python primitives and uses special JSON
    encoders and decoders to transform between datetimes and timedeltas and strings, and between
    numbers and decimals.

    Datetimes, timedeltas, and big numbers are represented as a dictionary with the structure:

        {"__class__": "{classname}", "__value__": "{string representation of vale}"}

    """

    def __init__(self):
        """Constructor."""
        self._dict_parser = DictParser()

    def serialise(self, expr: Expression) -> str:
        """Serialise an expression into a JSON string.

        Datetimes, timedeltas, and big numbers are represented as a dictionary with the structure:

            {"__class__": "{classname}", "__value__": "{string representation of vale}"}

        Args:
            expr: Expression to serialise.

        Returns:
            The expression serialised.
        """
        primitive_data = self._dict_parser.serialise(expr)
        json_str = json.dumps(primitive_data, cls=JSONExpressionEncoder)
        return json_str

    def parse(self, data: str) -> Expression:
        """Parse python literal data into an expression.

        If any value is a dictionary object with the structure:

            {"__class__": "{classname}", "__value__": "{string representation of vale}"}

        then the dictionary is converted in an instance of {classname}. Currently, only
        `bignumber`, `datetime` and `timedelta`  are recognised.

        Args:
            data: JSON string.

        Returns:
            Parsed expression.

        Raises:
            ParseException.
        """
        denormalised_data = json.loads(
            data,
            parse_int=Decimal,
            parse_float=Decimal,
            object_hook=expression_dict_decoder,
        )
        expr = self._dict_parser.parse(denormalised_data)
        return expr


class JSONExpressionEncoder(json.JSONEncoder):
    """Json encoder for python primitives representing expressions.

    The following conversions take place:

    * Decimals are serialised to numbers if no precision is lost. In other case, they are serialised
      as dictionary objects.
    * Types, datetimes and timedeltas are serialised as dictionary objects.

    Dictionary objects have the following structure:

        {"__class__": "{classname}", "__value__": <some-value>}
    """

    def default(self, o: Any) -> Any:  # pylint: disable=R0911
        """Encode object into a JSON serialisable value.

        * Decimals are serialised to numbers if no precision is lost. In other case, they are
          serialised as dictionary objects.
        * Types, datetimes and timedeltas are serialised as dictionary objects.

        Dictionary objects have the following structure:

            {"__class__": "{classname}", "__value__": <some-value>}
        """
        if isinstance(o, Decimal):
            num: int | float = int(o)
            if num == o:
                return num
            num = float(o)
            if str(num) == str(o):
                return num
            return {"__class__": "bignum", "__value__": str(o)}
        if isinstance(o, datetime):
            return {"__class__": "datetime", "__value__": o.isoformat()}
        if isinstance(o, timedelta):
            return {"__class__": "timedelta", "__value__": o.total_seconds()}
        if isinstance(o, type):
            return self.encode_type(o)
        return super().default(o)

    @staticmethod
    def encode_type(klass: type) -> dict:
        klass_name = klass.__name__
        klass_args: tuple[type] | None = getattr(klass, "__args__", None)
        encoded = {"__class__": "type", "__value__": klass_name}
        if klass_args is not None:
            encoded["__args__"] = [  # type: ignore
                JSONExpressionEncoder.encode_type(arg) for arg in klass_args
            ]
        return encoded


def expression_dict_decoder(obj: dict) -> Any:
    """Decode JSON dictionary representing python objects.

    If any value is a dictionary object with the structure:

        {"__class__": "{classname}", "__value__": <some-value>}

    then the dictionary is converted in an instance of {classname}. Currently, only
    types, `bignumber`, `datetime` and `timedelta`  are recognised.

    Note, dictionary objects must be used only for elements that cannot be represented by instances
    of Expression, like the value wrapped by literals, or
    """
    klass = obj.get("__class__", None)
    value = obj.get("__value__", None)
    if klass not in ["bignum", "datetime", "timedelta", "type"]:
        return obj
    if klass == "bignum":
        return Decimal(value)
    if klass == "datetime":
        return datetime.fromisoformat(value)
    if klass == "timedelta":
        return timedelta(seconds=float(value))
    if klass == "type":
        return dict_to_type(obj)
    # this is unreachable, added to make linting happy
    return obj


def dict_to_type(obj: dict) -> type:  # type: ignore  # pylint: disable=R0911
    """Convert a dictionary object into a type."""
    type_name: str | None = obj.get("__value__", None)
    args: list[dict] | None = obj.get("__args__", None)
    match type_name, args:
        case "null", _:
            return type(None)
        case "bool", _:
            return bool
        case "int", _:
            return int
        case "float", _:
            return float
        case "bignum", _:
            return Decimal
        case "str", _:
            return str
        case "datetime", _:
            return datetime
        case "timedelta", _:
            return timedelta
        case "tuple", None:
            return tuple
        case "list", None:
            return list
        case "dict", None:
            return dict
        case "tuple", args:
            return tuple[tuple((dict_to_type(o) for o in args))]  # type: ignore
        case "list", args:
            return list[tuple((dict_to_type(o) for o in args))]  # type: ignore
        case "dict", args:
            return dict[tuple((dict_to_type(o) for o in args))]  # type: ignore
        case _, _:
            raise RuntimeError("undecodable dictionary")

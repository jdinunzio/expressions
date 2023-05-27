from collections import deque
from typing import Any

from expressions.exceptions import ContextPopException, ContextVariableNotFoundException

# Marker to indicate no default has been specified (we can't use None, since that's a possible
# valid default).
NoDefault = object()


class Context:
    """Evaluation context.

    An evaluation context is a mapping from names to values. It allows the creation of a stack
    of sub-mappings that can be stacked.
    """

    def __init__(self, **mapping: Any):
        """Context constructor.

        Args:
            **mapping: Initial context mapping.
        """
        self._mappings: deque[dict[str, Any]] = deque()
        self._mappings.appendleft(mapping.copy())

    def get(self, name: str, default: Any = NoDefault) -> Any:
        """Return value of the given variable name in the first available mapping in the context.

        Args:
            name: Name of the variable to return.
            default: Optional value to return if name not in mapping.

        Returns:
            Value of the variable with the given name. If name not in mapping, return default.

        Raises:
            ContextVariableNotFound, if variable not in mapping, and no default specified.
        """
        for mapping in self._mappings:
            if name in mapping:
                return mapping[name]

        if default != NoDefault:
            return default

        raise ContextVariableNotFoundException(name)

    def set(self, name: str, value: Any) -> None:
        """Set value of variable in the topmost mapping in the context.

        Args:
            name: Name of the variable.
            value: Value of the variable.
        """
        self._mappings[0][name] = value

    def push_subcontext(self, **mapping: Any) -> None:
        """Push a new mapping in the context stack.

        Args:
            **mapping: Mapping to add at the top of the context stack.
        """
        self._mappings.appendleft(mapping.copy())

    def pop_subcontext(self) -> dict[str, Any]:
        """Pop the topmost mapping in the context stack.

        Returns:
            Topmost mapping in the stack.

        Raises:
            ContextPopException if there's no mapping to pop.
        """
        try:
            return self._mappings.popleft()
        except IndexError as exc:
            raise ContextPopException("No context to pop") from exc

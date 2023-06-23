class ExpressionError(Exception):
    """Base class for expression exceptions."""

    def __init__(self, message: str) -> None:
        """Expression Error constructor.

        Args:
            message: Error message.
        """
        super().__init__()
        self.message = message


class ExpressionValidationError(ExpressionError):
    """Expression Validation Error.

    Error raised during expression creation.
    """

    def __init__(self, message: str, errors: list[dict]) -> None:
        """Expression Validator Error constructor.

        Args:
            message: Error message.
            errors: List of validation errors.
        """
        super().__init__(message)
        self.errors = errors


class ExpressionEvaluationError(ExpressionError):
    """Expression Evaluation Error.

    Error raised when there's an error evaluating the expression.
    """


class VariableNotFoundError(ExpressionEvaluationError):
    """Variable not found during evaluation."""


class VariableTypeError(ExpressionEvaluationError):
    """Variable has wrong type."""


class ContextError(ExpressionError):
    """Base exception class for context related errors."""


class ContextVariableNotFoundError(ContextError):
    """Error raised when trying to access a variable not in context."""


class ContextPopError(ContextError):
    """Attempt to pop mapping from context with no mappings."""


class ParseError(ExpressionError):
    """Parse Error."""

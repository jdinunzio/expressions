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

    Exception raised during expression creation.
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

    Exception raised when there's an error evaluating the expression.
    """


class VariableNotFoundException(ExpressionEvaluationError):
    """Variable not found during evaluation."""


class VariableTypeException(ExpressionEvaluationError):
    """Variable has wrong type."""


class ContextException(ExpressionError):
    """Base exception class for context related errors."""


class ContextVariableNotFoundException(ContextException):
    """Exception raised when trying to access a variable not in context."""


class ContextPopException(ContextException):
    """Attempt to pop mapping from context with no mappings."""


class ParseException(ExpressionError):
    """Parse Exception."""

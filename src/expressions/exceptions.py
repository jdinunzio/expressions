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

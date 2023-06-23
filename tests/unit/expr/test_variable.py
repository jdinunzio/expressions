import unittest

from expressions import Context, Variable
from expressions.exceptions import VariableNotFoundError, VariableTypeError


class TestVariable(unittest.TestCase):
    """Test case for the Variable class."""

    def test_evaluate_with_variable_in_context(self):
        """evaluate() with a variable present in the context should return it."""
        context = Context(x=5)
        variable = Variable("x", int)
        result = variable.evaluate(context)
        self.assertEqual(result, 5)

    def test_evaluate_with_variable_not_in_context(self):
        """evaluate() with a variable not present in the context should raise."""
        context = Context()
        variable = Variable("x", int)
        with self.assertRaises(VariableNotFoundError):
            variable.evaluate(context)

    def test_evaluate_with_variable_in_context_and_default(self):
        """evaluate() with variable present in context and default value should return context."""
        context = Context(x=5)
        variable = Variable("x", int, default=10)
        result = variable.evaluate(context)
        self.assertEqual(result, 5)

    def test_evaluate_with_variable_in_context_wrong_type(self):
        """evaluate() with a variable present in the context but with the wrong type shout raise."""
        context = Context(x="hello")
        variable = Variable("x", int)
        with self.assertRaises(VariableTypeError):
            variable.evaluate(context)

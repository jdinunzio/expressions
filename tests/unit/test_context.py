import unittest

from expressions import Context
from expressions.exceptions import ContextPopError, ContextVariableNotFoundError


class ContextTests(unittest.TestCase):
    """Test case for Context."""

    def test_set_get_variable(self):
        """Variables can be set and get from context.

        Given an empty context,
        When a variable is set with a value,
        Then the value should be correctly retrieved from the context.
        """
        context = Context()
        context.set("x", 10)
        self.assertEqual(context.get("x"), 10)

    def test_get_variable_not_in_context_without_default(self):
        """Getting variables not defined in context without default should raise.

        Given an empty context,
        When trying to get a variable not present in the context,
        Then a ContextVariableNotFound exception should be raised.
        """
        context = Context()
        with self.assertRaises(ContextVariableNotFoundError):
            context.get("x")

    def test_get_variable_not_in_context_with_default(self):
        """Getting variables not defined in context with default should return default.

        Given an empty context,
        When trying to get a variable not present in the context with a default value,
        Then the default value should be returned.
        """
        context = Context()
        result = context.get("x", default=20)
        self.assertEqual(result, 20)

    def test_get_variable_in_subcontext(self):
        """Getting variable should return value in most recent subcontext.

        Given a context with a subcontext,
        When trying to get a variable present in the subcontext,
        Then the value of the variable should be retrieved correctly.
        """
        context = Context()
        context.push_subcontext(x=10)
        self.assertEqual(context.get("x"), 10)

    def test_get_variable_in_subcontext_overrides_parent_context(self):
        """Subcontext should override values in previous subcontext.

        Given a context with a variable defined,
        And a subcontext with the same variable defined with a different value,
        When trying to get the variable,
        Then the value from the subcontext should override the value in the parent context.
        """
        context = Context(x=5)
        context.push_subcontext(x=10)
        self.assertEqual(context.get("x"), 10)

    def test_pop_subcontext(self):
        """Popping a subcontext should return it.

        Given a context with a subcontext,
        When popping the subcontext,
        Then the subcontext should be removed from the stack and returned.
        """
        context = Context(x=5)
        self.assertEqual(len(context._mappings), 1)  # pylint: disable=protected-access
        mapping = context.pop_subcontext()
        self.assertIsInstance(mapping, dict)
        self.assertEqual(mapping, {"x": 5})
        self.assertEqual(len(context._mappings), 0)  # pylint: disable=protected-access

    def test_get_variable_old_value_visible_after_removing_contex(self):
        """Old values of variables should be visible after removing subcontext.

        Given a context with a variable defined,
        And a subcontext with the same variable defined with a different value,
        When the subcontext is popped,
        Then the value from the first subcontext should be visible again.
        """
        context = Context(x=5)
        context.push_subcontext(x=10)
        context.pop_subcontext()
        self.assertEqual(context.get("x"), 5)

    def test_pop_subcontext_last_context(self):
        """Popping a subcontext when there are no more subcontexts left should raise.

        Given a context with no subcontexts,
        When trying to pop a subcontext,
        Then a ContextPopException should be raised.
        """
        context = Context()
        context.pop_subcontext()
        with self.assertRaises(ContextPopError):
            context.pop_subcontext()

"""
Sample tests
"""
from django.test import SimpleTestCase


from app.calc import add, subtract


class CalcTests(SimpleTestCase):
    """Test the calc module."""

    def test_add_numbers(self):
        """Test adding numbers together."""
        res = add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        res = subtract(10, 15)
        self.assertEqual(res, 5)

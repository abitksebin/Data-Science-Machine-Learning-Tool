import unittest

from .context import sample


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_sample_fn(self):
        self.assertIsNone(sample.fn())


if __name__ == '__main__':
    unittest.main()

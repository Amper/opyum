import unittest

from opyum import *


class TestApp(unittest.TestCase):

    def test_decorator(self):
    	@optimize
        def test_func(a, b):
            return 1 + 2 + 3 * 4 + b + c
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


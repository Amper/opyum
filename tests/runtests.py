import os
import unittest


tests_loader = unittest.TestLoader()
test_suit = tests_loader.discover(os.path.abspath(os.path.dirname(__file__)))
unittest.TextTestRunner(verbosity = 2).run(test_suit)


import unittest

from opyum import *


class TestApp(unittest.TestCase):

    def test_mult_to_sum_1(self):
        src = ( "n = n * 0\n"
                "n = 0 * n\n"
                "n = n * 1\n"
                "n = 1 * n\n"
                "n = n * 2\n"
                "n = 2 * n\n"
                "n = n * 3\n"
                "n = 3 * n"
              )
        new_src = get_source\
                    ( value         = src
                    , optimized     = True
                    , optimizations = [ast_optimizations['MultToSum']]
                    )
        self.assertTrue(new_src == ( "n = 0\n"
                                     "n = 0\n"
                                     "n = n\n"
                                     "n = n\n"
                                     "n = (n + n)\n"
                                     "n = (n + n)\n"
                                     "n = (n * 3)\n"
                                     "n = (3 * n)"
                                   )
                       )


if __name__ == '__main__':
    unittest.main()


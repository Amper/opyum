import unittest

from opyum import *


class TestApp(unittest.TestCase):

    @staticmethod
    def optimize(source, optimization):
        return get_source\
                ( value         = source
                , optimized     = True
                , optimizations = [ast_optimizations[optimization]]
                )

    def test_mult_to_sum_0(self):
        for src_before in \
            ( "n = (n * 0)"
            , "n = (n * 0.0)"
            , "n = (0 * n)"
            , "n = (0.0 * n)"
            ):
            src_after = self.optimize(src_before, 'MultToSum')
            self.assertEqual("n = 0", src_after)
       
    def test_mult_to_sum_1(self):
        for src_before in \
            ( "n = (n * 1)"
            , "n = (n * 1.0)"
            , "n = (1 * n)"
            , "n = (1.0 * n)"
            ):
            src_after = self.optimize(src_before, 'MultToSum')
            self.assertEqual("n = n", src_after)

    def test_mult_to_sum_2(self):
        for src_before in \
            ( "n = (n * 2)"
            , "n = (n * 2.0)"
            , "n = (2 * n)"
            , "n = (2.0 * n)"
            ):
            src_after = self.optimize(src_before, 'MultToSum')
            self.assertEqual("n = (n + n)", src_after)

    def test_mult_to_sum_3(self):
        for src_before in \
            ( "n = (n * 3)"
            , "n = (n * 3.0)"
            , "n = (3 * n)"
            , "n = (3.0 * n)"
            ):
            src_after = self.optimize(src_before, 'MultToSum')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_0(self):
        for src_before in \
            ( "n = (n ** (- 0))"
            , "n = (n ** (- 0.0))"
            , "n = (n ** 0)"
            , "n = (n ** 0.0)"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual("n = 1", src_after)

    def test_pow_to_mult_0_5(self):
        for src_before in \
            ( "n = (n ** (- 0.5))"
            , "n = (n ** 0.5)"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_1(self):
        for src_before in \
            ( "n = (n ** (- 1))"
            , "n = (n ** (- 1.0))"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual("n = (1 / n)", src_after)
        for src_before in \
            ( "n = (n ** 1)"
            , "n = (n ** 1.0)"
            , "n = (n ** (+ 1))"
            , "n = (n ** (+ 1.0))"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual("n = n", src_after)

    def test_pow_to_mult_1_5(self):
        for src_before in \
            ( "n = (n ** (- 1.5))"
            , "n = (n ** 1.5)"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_2(self):
        for src_before in \
            ( "n = (n ** (- 2))"
            , "n = (n ** (- 2.0))"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual("n = (1 / (n * n))", src_after)
        for src_before in \
            ( "n = (n ** 2)"
            , "n = (n ** 2.0)"
            , "n = (n ** (+ 2))"
            , "n = (n ** (+ 2.0))"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual("n = (n * n)", src_after)

    def test_pow_to_mult_2_5(self):
        for src_before in \
            ( "n = (n ** (- 2.5))"
            , "n = (n ** 2.5)"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_3(self):
        for src_before in \
            ( "n = (n ** (- 3))"
            , "n = (n ** (- 3.0))"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual("n = (1 / ((n * n) * n))", src_after)
        for src_before in \
            ( "n = (n ** 3)"
            , "n = (n ** 3.0)"
            , "n = (n ** (+ 3))"
            , "n = (n ** (+ 3.0))"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual("n = ((n * n) * n)", src_after)

    def test_pow_to_mult_3_5(self):
        for src_before in \
            ( "n = (n ** (- 3.5))"
            , "n = (n ** 3.5)"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_4(self):
        for src_before in \
            ( "n = (n ** (- 4))"
            , "n = (n ** (- 4.0))"
            , "n = (n ** 4)"
            , "n = (n ** 4.0)"
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)


if __name__ == '__main__':
    unittest.main()


import unittest

from opyum import *
from timeit import timeit


class TestApp(unittest.TestCase):

    @staticmethod
    def optimize(source, optimization):
        return get_source\
                ( value         = source
                , optimized     = True
                , optimizations = [all_optimizations[optimization]]
                )

    def test_mult_to_sum_0(self):
        time_before = 0 
        time_after  = 0
        for src_before in \
            ( 'y = (x * 0)'
            , 'y = (x * 0.0)'
            , 'y = (0 * x)'
            , 'y = (0.0 * x)'
            ):
            src_after    = self.optimize(src_before, 'MultToSum')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = 0', src_after)
        self.assertGreaterEqual(time_before, time_after)
       
    def test_mult_to_sum_1(self):
        time_before = 0 
        time_after  = 0
        for src_before in \
            ( 'y = (x * 1)'
            , 'y = (x * 1.0)'
            , 'y = (1 * x)'
            , 'y = (1.0 * x)'
            ):
            src_after    = self.optimize(src_before, 'MultToSum')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = x', src_after)
        self.assertGreaterEqual(time_before, time_after)

    def test_mult_to_sum_2(self):
        # time_before = 0
        # time_after  = 0
        for src_before in \
            ( 'y = (x * 2)'
            , 'y = (x * 2.0)'
            , 'y = (2 * x)'
            , 'y = (2.0 * x)'
            ):
            src_after    = self.optimize(src_before, 'MultToSum')
            # time_before += timeit(src_before, setup="x = 10000")
            # time_after  += timeit(src_after , setup="x = 10000")
            # self.assertEqual('y = (x + x)', src_after)
            self.assertEqual(src_before, src_after)
        # self.assertGreaterEqual(time_before, time_after)

    def test_mult_to_sum_3(self):
        for src_before in ('y = (x * 3)', 'y = (3 * x)'):
            src_after = self.optimize(src_before, 'MultToSum')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_0(self):
        time_before = 0
        time_after  = 0
        for src_before in \
            ( 'y = (x ** (- 0))'
            , 'y = (x ** (- 0.0))'
            , 'y = (x ** 0)'
            , 'y = (x ** 0.0)'
            ):
            src_after    = self.optimize(src_before, 'PowToMult')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = 1', src_after)
        self.assertGreaterEqual(time_before, time_after)

    def test_pow_to_mult_0_5(self):
        for src_before in ('y = (x ** (- 0.5))', 'y = (x ** 0.5)'):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_1(self):
        time_before = 0
        time_after  = 0
        for src_before in ('y = (x ** (- 1))', 'y = (x ** (- 1.0))'):
            src_after    = self.optimize(src_before, 'PowToMult')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = (1 / x)', src_after)
        self.assertGreaterEqual(time_before, time_after)
        time_before = 0
        time_after  = 0
        for src_before in \
            ( 'y = (x ** 1)'
            , 'y = (x ** 1.0)'
            , 'y = (x ** (+ 1))'
            , 'y = (x ** (+ 1.0))'
            ):
            src_after    = self.optimize(src_before, 'PowToMult')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = x', src_after)
        self.assertGreaterEqual(time_before, time_after)

    def test_pow_to_mult_1_5(self):
        for src_before in ('y = (x ** (- 1.5))', 'y = (x ** 1.5)'):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_2(self):
        time_before = 0
        time_after  = 0
        for src_before in ('y = (x ** (- 2))', 'y = (x ** (- 2.0))'):
            src_after    = self.optimize(src_before, 'PowToMult')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = (1 / (x * x))', src_after)
        self.assertGreaterEqual(time_before, time_after)
        time_before = 0
        time_after  = 0
        for src_before in \
            ( 'y = (x ** 2)'
            , 'y = (x ** 2.0)'
            , 'y = (x ** (+ 2))'
            , 'y = (x ** (+ 2.0))'
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = (x * x)', src_after)
        self.assertGreaterEqual(time_before, time_after)

    def test_pow_to_mult_2_5(self):
        for src_before in ('y = (x ** (- 2.5))', 'y = (x ** 2.5)'):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_3(self):
        time_before = 0
        time_after  = 0
        for src_before in ('y = (x ** (- 3))', 'y = (x ** (- 3.0))'):
            src_after    = self.optimize(src_before, 'PowToMult')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = (1 / ((x * x) * x))', src_after)
        self.assertGreaterEqual(time_before, time_after)
        time_before = 0
        time_after  = 0
        for src_before in \
            ( 'y = (x ** 3)'
            , 'y = (x ** 3.0)'
            , 'y = (x ** (+ 3))'
            , 'y = (x ** (+ 3.0))'
            ):
            src_after    = self.optimize(src_before, 'PowToMult')
            time_before += timeit(src_before, setup="x = 10000")
            time_after  += timeit(src_after , setup="x = 10000")
            self.assertEqual('y = ((x * x) * x)', src_after)
        self.assertGreaterEqual(time_before, time_after)

    def test_pow_to_mult_3_5(self):
        for src_before in ('y = (x ** (- 3.5))', 'y = (x ** 3.5)'):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_pow_to_mult_4(self):
        for src_before in \
            ( 'y = (x ** (- 4))'
            , 'y = (x ** (- 4.0))'
            , 'y = (x ** 4)'
            , 'y = (x ** 4.0)'
            ):
            src_after = self.optimize(src_before, 'PowToMult')
            self.assertEqual(src_before, src_after)

    def test_yield_to_yield_from_1(self):
        src_wrapper  = 'def test(x):\n    {}\nr = sum(test(x))'
        src_before   = 'for y in range(x): yield y'
        src_after    = self.optimize(src_before, 'YieldToYieldFrom')
        src_before_w = src_wrapper.format(src_before)
        src_after_w  = src_wrapper.format(src_after)
        time_before  = timeit(src_before_w, setup="x = 10")
        time_after   = timeit(src_after_w , setup="x = 10")
        self.assertEqual("yield from range(x)", src_after)
        self.assertGreaterEqual(time_before, time_after)

    def test_yield_to_yield_from_2(self):
        src_before = 'for x in range(10):\n    yield (x + 1)'
        src_after  = self.optimize(src_before, 'YieldToYieldFrom')
        self.assertEqual(src_before, src_after)

    # def test_format_positions_1(self):
    #     src_before  = "'{}'.format(*x)"
    #     src_after   = self.optimize(src_before, 'FormatPositions')
    #     time_before = timeit(src_before, setup="x = [10000]")
    #     time_after  = timeit(src_after , setup="x = [10000]")
    #     self.assertEqual("''.format(*x)", src_after)
    #     self.assertGreaterEqual(time_before, time_after)

    # def test_format_positions_2(self):
    #     src_before  = "'_{}_{}_'.format(*x)"
    #     src_after   = self.optimize(src_before, 'FormatPositions')
    #     time_before = timeit(src_before, setup="x = [10000, 10]")
    #     time_after  = timeit(src_after , setup="x = [10000, 10]")
    #     self.assertEqual("'_{0}_{1}_'.format(*x)", src_after)
    #     self.assertGreaterEqual(time_before, time_after)

    # def test_format_positions_3(self):
    #     src_before  = "'{}{}{}'.format(*x)"
    #     src_after   = self.optimize(src_before, 'FormatPositions')
    #     time_before = timeit(src_before, setup="x = [10000, 10, 1]")
    #     time_after  = timeit(src_after , setup="x = [10000, 10, 1]")
    #     self.assertEqual("'{0}{1}{2}'.format(*x)", src_after)
    #     self.assertGreaterEqual(time_before, time_after)

    # def test_format_positions_4(self):
    #     src_before = "'{0}{}'.format(*args)"
    #     src_after = self.optimize(src_before, 'FormatPositions')
    #     self.assertEqual(src_before, src_after)

    # def test_format_positions_5(self):
    #     src_before = "'{}{1}'.format(*args)"
    #     src_after = self.optimize(src_before, 'FormatPositions')
    #     self.assertEqual(src_before, src_after)

    def test_constant_folding_1(self):
        src_before  = 'x += ((10 + 5 * 4 - 2) * 2 - 14)'
        src_after   = self.optimize(src_before, 'ConstantFolding')
        time_before = timeit(src_before, setup="x = 0")
        time_after  = timeit(src_after , setup="x = 0")
        self.assertEqual("x += 42", src_after)
        self.assertGreaterEqual(time_before, time_after)

    def test_constant_folding_2(self):
        src_before  = 'x += (((10 + 10) + (10 + 10)) + (10 + (10 + 10)) + ((10 + 10) + 10))'
        src_after   = self.optimize(src_before, 'ConstantFolding')
        time_before = timeit(src_before, setup="x = 0")
        time_after  = timeit(src_after , setup="x = 0")
        self.assertEqual("x += 100", src_after)
        self.assertGreaterEqual(time_before, time_after)


if __name__ == '__main__':
    unittest.main()


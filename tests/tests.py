import unittest

from opyum     import *
from timeit    import timeit
from itertools import repeat


class BaseTestCase(unittest.TestCase):

    @staticmethod
    def optimize(source, optimization):
        return get_source\
                ( value         = source
                , optimized     = True
                , optimizations = [all_optimizations[optimization]]
                )


class TestResults(BaseTestCase):

    def setUp(self):
        self.src_before    = ()
        self.optimizations = ()
        self.src_check     = ()

    def tearDown(self):
        if (self.src_before 
        and self.optimizations
        and self.src_check != ()
           ):
            if not isinstance(self.src_before, (list, tuple)):
                self.src_before = (self.src_before, )
            if not isinstance(self.src_check, (list, tuple)):
                self.src_check = repeat(self.src_check, times=len(self.src_before))
            if not isinstance(self.optimizations, (list, tuple)):
                self.optimizations = (self.optimizations, )
            for src_before, src_check in zip(self.src_before, self.src_check):
                src_after = src_before
                for optimization in self.optimizations:
                    src_after = self.optimize(src_after, optimization)
                self.assertEqual(src_check, src_after)
        else:
            self.assertTrue(False, msg='Not specified all the necessary parameters')
        self.src_before    = ()
        self.optimizations = ()
        self.src_check     = ()

    def test_mult_to_sum_0(self):
        self.optimizations = 'MultToSum'
        self.src_before    = ( 'y = (x * 0)'
                             , 'y = (x * 0.0)'
                             , 'y = (0 * x)'
                             , 'y = (0.0 * x)'
                             )
        self.src_check     = 'y = 0'
       
    def test_mult_to_sum_1(self):
        self.optimizations = 'MultToSum'
        self.src_before    = ( 'y = (x * 1)'
                             , 'y = (x * 1.0)'
                             , 'y = (1 * x)'
                             , 'y = (1.0 * x)'
                             )
        self.src_check     = 'y = x'

    def test_mult_to_sum_2(self):
        self.optimizations = 'MultToSum'
        self.src_before    = ( 'y = (x * 2)'
                             , 'y = (x * 2.0)'
                             , 'y = (2 * x)'
                             , 'y = (2.0 * x)'
                             )
        self.src_check     = 'y = (x + x)'

    def test_mult_to_sum_3(self):
        self.optimizations = 'MultToSum'
        self.src_before    = ( 'y = (x * 3)'
                             , 'y = (3 * x)'
                             )
        self.src_check     = self.src_before

    def test_pow_to_mult_0(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 0))'
                             , 'y = (x ** (- 0.0))'
                             , 'y = (x ** 0)'
                             , 'y = (x ** 0.0)'
                             )
        self.src_check     = 'y = 1'

    def test_pow_to_mult_0_5(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 0.5))'
                             , 'y = (x ** 0.5)'
                             )
        self.src_check     = self.src_before

    def test_pow_to_mult_1(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 1))'
                             , 'y = (x ** (- 1.0))'
                             , 'y = (x ** 1)'
                             , 'y = (x ** 1.0)'
                             , 'y = (x ** (+ 1))'
                             , 'y = (x ** (+ 1.0))'
                             )
        self.src_check     = ( ['y = (1 / x)'] * 2 
                             + ['y = x']       * 4
                             )

    def test_pow_to_mult_1_5(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 1.5))'
                             , 'y = (x ** 1.5)'
                             )
        self.src_check     = self.src_before

    def test_pow_to_mult_2(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 2))'
                             , 'y = (x ** (- 2.0))'
                             , 'y = (x ** 2)'
                             , 'y = (x ** 2.0)'
                             , 'y = (x ** (+ 2))'
                             , 'y = (x ** (+ 2.0))'
                             )
        self.src_check     = ( ['y = (1 / (x * x))'] * 2 
                             + ['y = (x * x)']       * 4
                             )

    def test_pow_to_mult_2_5(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 2.5))'
                             , 'y = (x ** 2.5)'
                             )
        self.src_check     = self.src_before

    def test_pow_to_mult_3(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 3))'
                             , 'y = (x ** (- 3.0))'
                             , 'y = (x ** 3)'
                             , 'y = (x ** 3.0)'
                             , 'y = (x ** (+ 3))'
                             , 'y = (x ** (+ 3.0))'
                             )
        self.src_check     = ( ['y = (1 / ((x * x) * x))'] * 2 
                             + ['y = ((x * x) * x)']       * 4
                             )

    def test_pow_to_mult_3_5(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 3.5))'
                             , 'y = (x ** 3.5)'
                             )
        self.src_check     = self.src_before

    def test_pow_to_mult_4(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 4))'
                             , 'y = (x ** (- 4.0))'
                             , 'y = (x ** 4)'
                             , 'y = (x ** 4.0)'
                             )
        self.src_check     = self.src_before

    def test_yield_to_yield_from_1(self):
        self.optimizations = 'YieldToYieldFrom'
        self.src_before    = 'for y in range(x): yield y'
        self.src_check     = 'yield from range(x)'

    def test_yield_to_yield_from_2(self):
        self.optimizations = 'YieldToYieldFrom'
        self.src_before    = 'for x in range(10):\n    yield (x + 1)'
        self.src_check     = self.src_before

    def test_format_positions_1(self):
        self.optimizations = 'FormatPositions'
        self.src_before    = "'{}'.format(*x)"
        self.src_check     = "'{0}'.format(*x)"

    def test_format_positions_2(self):
        self.optimizations = 'FormatPositions'
        self.src_before    = "'_{}_{}_'.format(*x)"
        self.src_check     = "'_{0}_{1}_'.format(*x)"

    def test_format_positions_3(self):
        self.optimizations = 'FormatPositions'
        self.src_before    = "'{}{}{}'.format(*x)"
        self.src_check     = "'{0}{1}{2}'.format(*x)"

    def test_format_positions_4(self):
        self.optimizations = 'FormatPositions'
        self.src_before    = "'{0}{}'.format(*args)"
        self.src_check     = self.src_before

    def test_format_positions_5(self):
        self.optimizations = 'FormatPositions'
        self.src_before    = "'{}{1}'.format(*args)"
        self.src_check     = self.src_before

    def test_constant_folding_1(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = 'x += ((10 + 5 * 4 - 2) * 2 - 14)'
        self.src_check     = 'x += 42'

    def test_constant_folding_2(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = 'x += (((10 + 10) + (10 + 10)) + (10 + (10 + 10)) + ((10 + 10) + 10))'
        self.src_check     = 'x += 100'

    def test_constant_folding_3(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = 'x = [(i + 1) for i in range(0, 20, 2) if ((i % 3) != 0)]'
        self.src_check     = 'x = [3, 5, 9, 11, 15, 17]'

    def test_constant_folding_4(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = ( 'x = 7 * 24 * 60 * 60'
                             , 'y = [(i ** 2) for i in range(10) if ((i % 2) == 0)]'
                             , 'z = sum(range(1000))'
                             )
        self.src_check     = ( 'x = 604800'
                             , 'y = [0, 4, 16, 36, 64]'
                             , 'z = 499500'
                             )

    def test_builtin_const_propagation_and_folding_1(self):
        self.optimizations = ('BuiltinConstantPropagation', 'ConstantFolding')
        self.src_before    = 'from math import pi\ny = sum(map((lambda r: (2 * pi * r)), range(x)))'
        self.src_check     = 'from math import pi\ny = sum(map((lambda r: (6.283185307179586 * r)), range(x)))'

    def test_dead_code_elimination_1(self):
        self.optimizations = 'DeadCodeElimination'
        self.src_before    = '\n'.join( ( 'if condition:'
                                        , '    do_something()'
                                        , 'else:'
                                        , '    pass'          
                                      ) )
        self.src_check     = '\n'.join( ( 'if condition:'
                                        , '    do_something()'
                                      ) )

    def test_dead_code_elimination_2(self):
        self.optimizations = 'DeadCodeElimination'
        self.src_before    = '\n'.join( ( 'if condition:'
                                        , '    pass'
                                        , 'else:'
                                        , '    do_something()'
                                      ) )
        self.src_check     = '\n'.join( ( 'if (not condition):'
                                        , '    do_something()'
                                      ) )

    def test_dead_code_elimination_3(self):
        self.optimizations = 'DeadCodeElimination'
        self.src_before    = '\n'.join( ( 'if condition1:'
                                        , '    pass'
                                        , 'elif condition2:'
                                        , '    pass'
                                        , 'else:'
                                        , '    pass'
                                        , 'do_something()'
                                      ) )
        self.src_check     = 'do_something()'

    def test_dead_code_elimination_4(self):
        self.optimizations = 'DeadCodeElimination'
        self.src_before    = '\n'.join( ( 'if condition1:'
                                        , '    pass'
                                        , 'elif condition2:'
                                        , '    do_something1()'
                                        , 'else:'
                                        , '    do_something2()'
                                      ) )
        self.src_check     = '\n'.join( ( 'if ((not condition1) and condition2):'
                                        , '    do_something1()'
                                        , 'else:'
                                        , '    do_something2()'
                                      ) )

    def test_dead_code_elimination_5(self):
        self.optimizations = 'DeadCodeElimination'
        self.src_before    = '\n'.join( ( 'if condition1:'
                                        , '    pass'
                                        , 'elif condition2:'
                                        , '    do_something()'
                                        , 'else:'
                                        , '    pass'
                                      ) )
        self.src_check     = '\n'.join( ( 'if ((not condition1) and condition2):'
                                        , '    do_something()'
                                      ) )

    def test_dead_code_elimination_6(self):
        self.optimizations = 'DeadCodeElimination'
        self.src_before    = '\n'.join( ( 'if condition1:'
                                        , '    pass'
                                        , 'elif condition2:'
                                        , '    pass'
                                        , 'else:'
                                        , '    do_something()'
                                      ) )
        self.src_check     = '\n'.join( ( 'if ((not condition1) and (not condition2)):'
                                        , '    do_something()'
                                      ) )


class Benchmarks(BaseTestCase):

    def setUp(self):
        self.time_before   = 0 
        self.time_after    = 0
        self.src_before    = ()
        self.optimizations = ()
        self.set_up        = None

    def tearDown(self):
        if self.src_before and self.optimizations:
            if not isinstance(self.src_before, (list, tuple)):
                self.src_before = (self.src_before, )
            if not isinstance(self.optimizations, (list, tuple)):
                self.optimizations = (self.optimizations, )
            for src_before in self.src_before:
                src_after = src_before
                for optimization in self.optimizations:
                    src_after     = self.optimize(src_after, optimization)
                self.time_before += timeit(src_before, setup=self.set_up)
                self.time_after  += timeit(src_after , setup=self.set_up)
            self.assertGreaterEqual(self.time_before, self.time_after)
        self.time_before   = 0 
        self.time_after    = 0
        self.src_before    = ()
        self.optimizations = ()
        self.set_up        = None

    def test_mult_to_sum_0(self):
        self.optimizations = 'MultToSum'
        self.src_before    = ( 'y = (x * 0)'
                             , 'y = (x * 0.0)'
                             , 'y = (0 * x)'
                             , 'y = (0.0 * x)'
                             )
        self.set_up        = "x = 10000"
       
    def test_mult_to_sum_1(self):
        self.optimizations = 'MultToSum'
        self.src_before    = ( 'y = (x * 1)'
                             , 'y = (x * 1.0)'
                             , 'y = (1 * x)'
                             , 'y = (1.0 * x)'
                             )
        self.set_up        = "x = 10000"

    def test_mult_to_sum_2(self):
        self.optimizations = 'MultToSum'
        self.src_before    = ( 'y = (x * 2)'
                             , 'y = (x * 2.0)'
                             , 'y = (2 * x)'
                             , 'y = (2.0 * x)'
                             )
        self.set_up        = "x = 10000"

    def test_pow_to_mult_0(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 0))'
                             , 'y = (x ** (- 0.0))'
                             , 'y = (x ** 0)'
                             , 'y = (x ** 0.0)'
                             )
        self.set_up        = "x = 10000"

    def test_pow_to_mult_1(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 1))'
                             , 'y = (x ** (- 1.0))'
                             , 'y = (x ** 1)'
                             , 'y = (x ** 1.0)'
                             , 'y = (x ** (+ 1))'
                             , 'y = (x ** (+ 1.0))'
                             )
        self.set_up        = "x = 10000"

    def test_pow_to_mult_2(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 2))'
                             , 'y = (x ** (- 2.0))'
                             , 'y = (x ** 2)'
                             , 'y = (x ** 2.0)'
                             , 'y = (x ** (+ 2))'
                             , 'y = (x ** (+ 2.0))'
                             )
        self.set_up        = "x = 10000"

    def test_pow_to_mult_3(self):
        self.optimizations = 'PowToMult'
        self.src_before    = ( 'y = (x ** (- 3))'
                             , 'y = (x ** (- 3.0))'
                             , 'y = (x ** 3)'
                             , 'y = (x ** 3.0)'
                             , 'y = (x ** (+ 3))'
                             , 'y = (x ** (+ 3.0))'
                             )
        self.set_up        = "x = 10000"

    def test_yield_to_yield_from_1(self):
        self.optimizations = 'YieldToYieldFrom'
        self.src_before    = 'def test(x):\n    for y in range(x): yield y\nr = sum(test(x))'
        self.set_up        = "x = 10"

    #def test_format_positions_1(self):
    #    self.optimizations = 'FormatPositions'
    #    self.src_before    = "'{}'.format(*x)"
    #    self.set_up        = "x = [10000]"

    #def test_format_positions_2(self):
    #    self.optimizations = 'FormatPositions'
    #    self.src_before    = "'_{}_{}_'.format(*x)"
    #    self.set_up        = "x = [10000, 100000]"

    #def test_format_positions_3(self):
    #    self.optimizations = 'FormatPositions'
    #    self.src_before    = "'{}{}{}'.format(*x)"
    #    self.set_up        = "x = [10000, 100000, 1000000]"

    def test_constant_folding_1(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = 'x += ((10 + 5 * 4 - 2) * 2 - 14)'
        self.set_up        = 'x = 0'

    def test_constant_folding_2(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = 'x += (((10 + 10) + (10 + 10)) + (10 + (10 + 10)) + ((10 + 10) + 10))'
        self.set_up        = 'x = 0'

    def test_constant_folding_3(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = 'x += sum([(i + 1) for i in range(0, 20, 2) if ((i % 3) != 0)])'
        self.set_up        = 'x = 0'

    def test_constant_folding_4(self):
        self.optimizations = 'ConstantFolding'
        self.src_before    = ( 'x = 7 * 24 * 60 * 60'
                             , 'y = [(i ** 2) for i in range(10) if ((i % 2) == 0)]'
                             , 'z = sum(range(1000))'
                             )
        self.set_up        = ''

    def test_builtin_const_propagation_and_folding_1(self):
        self.optimizations = ('BuiltinConstantPropagation', 'ConstantFolding')
        self.src_before    = 'from math import pi\ny = sum(map((lambda r: (2 * pi * r)), range(x)))'
        self.set_up        = 'x = 10'


if __name__ == '__main__':
    unittest.main(verbosity = 2)


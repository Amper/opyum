"""

"""


import ast
import operator
from . import ASTOptimization


class ConstantFolding(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Constant folding'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 1

    _operators = \
        { ast.Add	  : operator.add
        , ast.Sub	  : operator.sub
        , ast.Mult    : operator.mul
        , ast.FloorDiv: operator.floordiv
        , ast.Div     : operator.truediv
        , ast.Pow 	  : operator.pow
        , ast.LShift  : operator.lshift
        , ast.RShift  : operator.rshift
        , ast.Mod     : operator.mod
        }

    def visit_BinOp(self, node):
        node  = self.generic_visit(node)
        left  = node.left
        right = node.right
        if all(isinstance(value, ast.Num) for value in (left, right)):
            if type(node.op) in self._operators:
                val  = self._operators[type(node.op)](left.n, right.n)
                node = ast.copy_location(ast.Num(n = val), node)
        elif all(isinstance(value, ast.Str) for value in (left, right)):
           if isinstance(node.op, ast.Add):
                val  = left.s + left.s
                node = ast.copy_location(ast.Str(s = val), node)
        return node

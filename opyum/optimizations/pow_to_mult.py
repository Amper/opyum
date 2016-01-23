"""

"""


import ast
from copy import copy
from . import ASTOptimization


class PowToMult(ASTOptimization):
    """

    """

    MAX_DEGREE = 5

    @property
    def name(self) -> str:
        return 'Power to multiplication'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 2

    def _is_numeric_pow(self, node: ast.BinOp) -> bool:
        if isinstance(node.op, ast.Pow):
            if  isinstance(node.left, (ast.Name, ast.Num)) \
            and isinstance(node.right, ast.Num):
                degree = node.right.n
                if isinstance(degree, float):
                    degree = int(degree) if degree.is_integer() else degree
                return isinstance(degree, int)
        return False

    def visit_BinOp(self, node: ast.BinOp):
        node = self.generic_visit(node)
        if self._is_numeric_pow(node):
            left, right  = node.left, node.right
            if right.n == 0:
                node = ast.copy_location(ast.Num(n = 1), node)
            elif right.n == 1:
                node = node.left
            elif 2 <= right.n <= self.MAX_DEGREE:
                for num in range(1, node.right.n):
                    new_node = ast.BinOp(left = left, op = ast.Mult(), right = copy(node.left))
                    left = node = ast.copy_location(new_node, node)
        return node

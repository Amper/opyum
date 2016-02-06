"""

"""


import ast
from copy import copy
from . import ASTOptimization


class MultToSum(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Multiplication to sum'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 2

    def _is_numeric_mult(self, node: ast.BinOp) -> bool:
        if isinstance(node.op, ast.Mult):
            if  isinstance(node.left , (ast.Name, ast.Num)) \
            and isinstance(node.right, ast.Num):
                return True
            if  isinstance(node.right, (ast.Name, ast.Num)) \
            and isinstance(node.left , ast.Num):
                return True
        return False

    def visit_BinOp(self, node: ast.BinOp) -> ast.BinOp:
        node = self.generic_visit(node)
        if self._is_numeric_mult(node):
            if isinstance(node.right, ast.Num):
                if node.right.n == 0:
                    node       = ast.copy_location(ast.Num(n = 0), node)
                elif node.right.n == 1:
                    node       = node.left
                elif node.right.n == 2:
                    node.op    = ast.copy_location(ast.Add(), node.op)
                    node.right = copy(node.left)
            elif isinstance(node.left , ast.Num):
                if node.left.n == 0:
                    node       = ast.copy_location(ast.Num(n = 0), node)
                elif node.left.n == 1:
                    node       = node.right
                elif node.left.n == 2:
                    node.op    = ast.copy_location(ast.Add(), node.op)
                    node.left  = copy(node.right)
        return node
"""

"""


import ast
from copy import copy
from . import ASTOptimization


class PowToMult(ASTOptimization):
    """

    """

    MAX_DEGREE = 3

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
            left, right = node.left, node.right
            if isinstance(left, (ast.Name, ast.Num)):
                if isinstance(right, ast.Num):
                    degree = right.n
                elif isinstance(right, ast.UnaryOp)\
                and  isinstance(right.op, (ast.USub, ast.UAdd))\
                and  isinstance(right.operand, ast.Num):
                    degree = right.operand.n
                else:
                    return False
                if isinstance(degree, float):
                    degree = int(degree) if degree.is_integer() else degree
                return isinstance(degree, int)
        return False

    def visit_BinOp(self, node: ast.BinOp):
        node = self.generic_visit(node)
        if self._is_numeric_pow(node):
            left, right = node.left, node.right
            degree = (    right.n         if isinstance(right, ast.Num) 
                    else -right.operand.n if isinstance(right.op, ast.USub) 
                    else  right.operand.n )
            degree = int(degree)
            if abs(degree) == 0:
                node = ast.copy_location(ast.Num(n = 1), node)
            elif abs(degree) == 1:
                node = node.left
            elif 2 <= abs(degree) <= self.MAX_DEGREE:
                for _ in range(1, abs(degree)):
                    new_node = ast.BinOp\
                                ( left = left
                                , op = ast.Mult()
                                , right = copy(node.left)
                                )
                    left = new_node = ast.copy_location(new_node, node)
                node = new_node
            else:
                return node
            if degree < 0:
                new_node = ast.BinOp\
                                ( left  = ast.Num(n = 1)
                                , op    = ast.Div()
                                , right = node 
                                )
                node = ast.copy_location(new_node, node)
        return node

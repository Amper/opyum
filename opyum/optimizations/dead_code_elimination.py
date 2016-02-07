"""

"""


import ast
import operator
from collections import deque
from . import ASTOptimization


class DeadCodeElimination(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Dead code elimination'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 1

    def visit_If(self, node):
        node = self.generic_visit(node)
        if (node.orelse 
        and len(node.orelse) == 1 
        and isinstance(node.orelse[0], ast.Pass)
           ):
            node.orelse = []
        if (len(node.body) == 1
        and isinstance(node.body[0], ast.Pass)
           ):
            if node.orelse:
                node_test = ast.UnaryOp(op=ast.Not(), operand=node.test)
                if (len(node.orelse) == 1
                and isinstance(node.orelse[0], ast.If)
                   ):
                    node_test   = ast.BoolOp\
                                        ( op     = ast.And()
                                        , values = [node_test, node.orelse[0].test]
                                        )
                    node.test   = ast.copy_location(node_test, node.orelse[0].test)
                    node.body   = node.orelse[0].body
                    node.orelse = node.orelse[0].orelse
                else:
                    node.test   = ast.copy_location(node_test, node.test)
                    node.body   = node.orelse
                    node.orelse = []
            else:
                node = None
        return node


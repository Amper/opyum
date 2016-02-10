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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node_level   = 0
        self._return_level = None

    def visit(self, node):
        if self._return_level:
            if self._node_level == self._return_level:
                return None
            elif self._node_level < self._return_level:
                self._return_level = None
        if isinstance(node, ast.Return):
            self._return_level = self._node_level
        self._node_level += 1
        node = super().visit(node)
        self._node_level -= 1
        return node

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



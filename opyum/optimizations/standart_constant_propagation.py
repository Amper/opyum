"""

"""


import ast
import math
from copy import copy
from . import ASTOptimization



class StandartConstantPropagation(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Standart constant propagation'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._constants = {}

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            if node.id in self._constants:
                node = ast.copy_location(self._constants[node.id], node)
        return node

    def visit_Attribute(self, node: ast.Attribute):
        node = self.generic_visit(node)
        if isinstance(node.value, ast.Name):
            if isinstance(node.ctx, ast.Load):
                name = '{}.{}'.format(node.value.id, node.attr)
                if name in self._constants:
                    node = ast.copy_location(self._constants[name], node)
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        node = self.generic_visit(node)
        if node.module in ('math', ):
            for alias in node.names:
                if alias.name in ('pi', 'e') and not alias.asname:
                    self._constants[alias.name] = ast.Num(n = getattr(math, alias.name))
        return node

    def visit_Import(self, node: ast.Import) -> ast.Import:
        node = self.generic_visit(node)
        for alias in node.names:
            if alias.name == 'math' and not alias.asname:
                self._constants['math.pi'] = ast.Num(n = math.pi)
                self._constants['math.e']  = ast.Num(n = math.e)
        return node


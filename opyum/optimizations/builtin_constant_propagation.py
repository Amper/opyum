"""

"""


import ast
import math
from copy import copy
from collections import defaultdict
from . import ASTOptimization



class BuiltinConstantPropagation(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Builtin constant propagation'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 3

    _constants = defaultdict(set)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._values = {}
        self.add_constant('math', 'pi')
        self.add_constant('math', 'e')

    @classmethod
    def add_constant(cls, module, name):
        cls._constants[module].add(name)

    def _add_value(self, module, name, alias):
        module = __import__(module)
        value  = getattr(module, name)
        if isinstance(value, (int, float)):
            self._values[alias] = ast.Num(n = value)

    def visit_Module(self, node: ast.Module):
        self._values = {}
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            if node.id in self._values:
                node = ast.copy_location(self._values[node.id], node)
        return node

    def visit_Attribute(self, node: ast.Attribute):
        if isinstance(node.value, ast.Name):
            if isinstance(node.ctx, ast.Load):
                name = '{}.{}'.format(node.value.id, node.attr)
                if name in self._values:
                    node = ast.copy_location(self._values[name], node)
        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:
        const = self.__class__._constants
        if node.module in const:
            for alias in node.names:
                if alias.name in const[node.module] and not alias.asname:
                    self._add_value(node.module, alias.name, alias.name)
        return self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> ast.Import:
        const = self.__class__._constants
        for module in node.names:
            if module.name in const and not module.asname:
                for name in const[module.name]:
                    self._add_value(module.name, name, '{}.{}'.format(module.name, name))
        return self.generic_visit(node)


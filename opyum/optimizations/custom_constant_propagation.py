"""

"""


import ast
from . import ASTOptimization


class CustomConstantPropagation(ASTOptimization):
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
        return 4

    def is_const_name(self, name):
        """

        """
        return name.startswith('C_') and name.isupper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._constants = {}

    def visit_Module(self, node):
        for expr in node.body:
            if not isinstance(expr, ast.Assign):
                continue
            if not isinstance(expr.value, (ast.Num, ast.Str)):
                continue
            if len(expr.targets) != 1:
                continue
            name = expr.targets[0]
            if not isinstance(name, ast.Name):
                continue
            name = name.id
            if not self.is_const_name(name):
                continue
            if name in self._constants:
                self._constants[name] = None
            else:
                self._constants[name] = expr.value
        return self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            node = self._constants.get(node.id) or node
        return node


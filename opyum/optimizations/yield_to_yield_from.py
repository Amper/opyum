"""

"""


import ast
from . import ASTOptimization


class YieldToYieldFrom(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Yield to "yield from"'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 3

    def _is_for_yield(self, node: ast.For) -> bool:
        if node.orelse:
            return False
        if not isinstance(node.target, ast.Name):
            return False
        body = node.body
        if len(body) != 1:
            return False
        expr = body[0]
        if not isinstance(expr, ast.Expr):
            return False
        yield_ = expr.value
        if not isinstance(yield_, ast.Yield):
            return False
        name = yield_.value
        if not isinstance(name, ast.Name):
            return False
        if name.id != node.target.id:
            return False
        return True

    def visit_For(self, node: ast.For):
        node = self.generic_visit(node)
        if self._is_for_yield(node):
            yield_node = ast.YieldFrom(value = node.iter)
            expr_node = ast.Expr(value = yield_node)
            node = ast.copy_location(expr_node, node)
            node = ast.fix_missing_locations(node)
        return node
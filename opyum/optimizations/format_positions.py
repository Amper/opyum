"""

"""


# import ast
# from . import ASTOptimization


# class FormatPositions(ASTOptimization):
#     """

#     """

#     @property
#     def name(self) -> str:
#         return '...'

#     @property
#     def description(self) -> str:
#         return ''

#     @property
#     def level(self) -> int:
#         return 5

#     def visit_Call(self, node: ast.Call) -> ast.Call:
#         node = self.generic_visit(node)
#         if (node.args or node.starargs) and not (node.keywords or node.kwargs):
#             func = node.func
#             if isinstance(func, ast.Attribute):
#                 if func.attr == 'format' and isinstance(func.ctx, ast.Load):
#                     if isinstance(func.value, ast.Str):
#                         s = node.func.value.s
#                         positions = ['{' + str(n) + '}' for n in range(0, s.count('{'))]
#                         try:
#                             node.func.value.s = s.format(*positions)
#                         except (ValueError, IndexError) as exc:
#                             pass
#         return node
"""

"""


import ast
from . import ASTOptimization


class MapToGenerator(ASTOptimization):
    """

    """

    _iter_name = '_UniqueMapToGeneratorIteratorName2d9DF4fgdG37fF58'

    @property
    def name(self) -> str:
        return 'Map to generator'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 5

    def _is_map(self, node: ast.Call) -> bool:
        if isinstance(node.func, ast.Name):
            if node.func.id == 'map':
                if len(node.args) == 2:
                    return True
            return False

    def visit_Call(self, node: ast.Call):
        node = self.generic_visit(node)
        if self._is_map(node):
            func, lst = node.args
            new_node = ast.GeneratorExp\
                            ( elt = ast.Call
                                        ( func     = func
                                        , args     = ast.Name
                                                        ( id  = self._iter_name
                                                        , ctx = ast.Load()
                                                        )
                                        , keywords = []
                                        , starargs = None
                                        , kwargs   = None
                                        )
                            , generators = 	[ ast.comprehension
                                                ( target =
                                                     ast.Name
                                                        ( id  = self._iter_name
                                                        , ctx = ast.Load()
                                                        )
                                                )
                                            ]
                            , iter = lst
                            )
            node = ast.copy_location(ast.Expr(value = new_node), node)
        return node
        
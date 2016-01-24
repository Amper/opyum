"""

"""


import ast
from . import ASTOptimization


class GlobalsToLocals(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Globals to locals'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._namespaces = []

    def visit_FunctionDef(self, node):

        _globals = {}
        _locals  = {}
        _new     = {}

        args  = node.args
        varg  = args.vararg
        kwoa  = args.kwonlyargs
        kwdef = args.kw_defaults
        kwarg = args.kwarg
        args  = args.args

        _locals.update({arg.arg  : arg   for arg   in args})
        _locals.update({arg.arg  : arg   for arg   in kwoa})
        _locals.update({varg.arg : varg } if varg  else {})
        _locals.update({kwarg.arg: kwarg} if kwarg else {})
        _locals.update({node.name: node})

        self._namespaces.append\
            ( { 'locals' : _locals
              , 'globals': _globals
              , 'node'   : node
              , 'new'    : _new
            } )
        node = self.generic_visit(node)
        ns   = self._namespaces.pop()

        changed = False
        for name in (_ for _, count in ns['new'].items() if count > 1):
            kwoa.append(ast.arg(arg=name, annotation=None))
            kwdef.append(ast.Name(id=name, ctx=ast.Load()))
        else:
            return node

        node.args.kwonlyargs  = kwoa
        node.args.kw_defaults = kwdef

        return node

    def visit_Name(self, node):
        if self._namespaces:
            ns = self._namespaces[-1]
            if isinstance(node.ctx, ast.Store):
                ns['locals'][node.id] = node
            elif isinstance(node.ctx, ast.Load):
                if node.id not in ns['locals']:
                    cnt = ns['new'].get(node.id, 0)
                    ns['new'][node.id] = cnt + 1
        return self.generic_visit(node)

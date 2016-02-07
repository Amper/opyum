"""

"""


import ast
import operator
from collections import deque
from . import ASTOptimization


class ConstantFolding(ASTOptimization):
    """

    """

    @property
    def name(self) -> str:
        return 'Constant folding'

    @property
    def description(self) -> str:
        return ''

    @property
    def level(self) -> int:
        return 1

    _operators = \
        { ast.Add	  : operator.add
        , ast.Sub	  : operator.sub
        , ast.Mult    : operator.mul
        , ast.FloorDiv: operator.floordiv
        , ast.Div     : operator.truediv
        , ast.Pow 	  : operator.pow
        , ast.LShift  : operator.lshift
        , ast.RShift  : operator.rshift
        , ast.Mod     : operator.mod
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_names    = deque()
        self._iter_targets = set()

    def convert(self, node):
        code     = compile(node, '<string>', mode = 'eval')
        value    = eval(code)
        new_node = ast.parse(str(value), mode = 'eval')
        if isinstance(new_node, ast.Expression):
            new_node = new_node.body
        new_node = self.generic_visit(new_node)
        node     = ast.copy_location(new_node, node)
        node     = ast.fix_missing_locations(node)
        return node

    def fold(self, node):
        self._has_names.append(False)
        node = self.generic_visit(node)
        if not self._has_names.pop():
            try:
                node = self.convert(node)
            except TypeError as exc:
                if  not isinstance(node, ast.Expression) \
                and str(exc).startswith('expected Expression node, got'):
                    try:
                        node = self.convert(ast.Expression(body=node))
                    except:
                        pass
            except:
                pass
        return node

    def comprehension(self, node):
        iter_targets = set(g.target.id for g in node.generators)
        self._iter_targets |= iter_targets
        node = self.fold(node)
        self._iter_targets -= iter_targets
        return node

    def visit_BinOp(self, node):
        node  = self.generic_visit(node)
        left  = node.left
        right = node.right
        if all(isinstance(value, ast.Num) for value in (left, right)):
            if isinstance(node.op, tuple(self._operators.keys())):
                val  = self._operators[type(node.op)](left.n, right.n)
                node = ast.copy_location(ast.Num(n = val), node)
                return node
        elif all(isinstance(value, ast.Str) for value in (left, right)):
           if isinstance(node.op, ast.Add):
                val  = left.s + right.s
                node = ast.copy_location(ast.Str(s = val), node)
                return node
        return self.fold(node)

    #def visit_GeneratorExp(self, node):
    #    return self.comprehension(node)

    def visit_ListComp(self, node):
        return self.comprehension(node)

    def visit_DictComp(self, node):
        return self.comprehension(node)

    def visit_Call(self, node):
        return self.fold(node)

    def visit_Name(self, node):
        if  self._has_names \
        and not (  node.id in __builtins__
                or not isinstance(node.ctx, ast.Load)
                or node.id in self._iter_targets
                ):
            self._has_names.pop()
            self._has_names.append(True)
        return self.generic_visit(node)

"""

"""


import ast
import functools
import types
import inspect

from .decompile import to_ast
from .compile import from_ast
from .optimizations import BasicOptimization


__all__ = \
        [ "optimize"
        , "get_source"
        ]


def transform(value, transformers, file=None):
    """

    :param value:
    :param transformers:
    :return:
    """

    result = value

    if transformers:
        node = to_ast(value, file=file)
        if node:
            for transformer in transformers:
                node = transformer.visit(node)
                node = ast.fix_missing_locations(node)
            result = from_ast(node, value)

    return result


def optimize\
    ( optimizations: (BasicOptimization, type, list, tuple) = None
    , level: (float, int) = None
    , classes: tuple = None
    , file: str = None
    , value = None
    ):

    """

    :param optimizations:
    :param level:
    :param classes:
    :param value:
    :return:
    """

    if optimizations and not value and isinstance(optimizations, types.FunctionType):
        optimizations, value = value, optimizations

    if optimizations:
        if not isinstance(optimizations, (list, tuple)):
            optimizations = (optimizations, )
    else:
        optimizations = (opt for _, opt in BasicOptimization.optimizations.items())

    optimizations = (op if isinstance(op, classes or (BasicOptimization, )) else op() for op in optimizations)

    if level:
        optimizations = (op for op in optimizations if op.level <= level)

    if value:
        result = transform(value, optimizations, file=file)
    else:
        result = functools.partial(transform, transformers=optimizations, file=file)

    return result


def get_source\
    ( value
    , optimized: bool = False
    , optimizations: (BasicOptimization, type, list, tuple) = None
    , level: (float, int) = None
    , classes: tuple = None
    ):

    """

    """

    if not value:
        return ""

    if optimized:
        try:
            file = inspect.getfile(value)
        except TypeError:
            file = None
        value = optimize\
                ( optimizations = optimizations
                , level         = level
                , classes       = classes
                , file          = file
                , value         = value
                )
    
    tree   = to_ast(value)
    result = ast_to_code(tree)

    return result




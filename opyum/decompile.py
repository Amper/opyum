"""

"""


import ast
import inspect
import types
import functools

from .utils import _call_with_frames_removed


__all__ = \
        [ "to_ast"
        , "code_to_ast"
        , "func_to_ast"
        , "source_to_ast"
        , "module_to_ast"
        , "node_to_ast"
        , "class_to_ast"
        , "method_to_ast"
        ]


@functools.singledispatch
def to_ast(value, file: str = None) -> ast.AST:
    """
    Returns node object for any value.
    """
    raise TypeError('Unexpected type for value: {}'.format(str(type(value))))


@to_ast.register(types.CodeType)
def code_to_ast(code: types.CodeType, file: str = None) -> ast.Module:
    """
    Return node object for code object.
    """

    if code and not isinstance(code, types.CodeType):
        raise TypeError('Unexpected type: {}'.format(str(type(code))))

    result = None

    try:
        src = inspect.getsource(code)
        file = file or inspect.getfile(code)
        result = source_to_ast(src, file)
    except IOError:
        pass

    return result


@to_ast.register(types.FunctionType)
def func_to_ast(func: types.FunctionType, file: str = None) -> ast.Module:
    """
    Return node object for function.
    """

    if func and not isinstance(func, types.FunctionType):
        raise TypeError('Unexpected type: {}'.format(str(type(func))))

    result = None

    if func and hasattr(func, '__code__'):
        result = code_to_ast(func.__code__, file)

    return result


@to_ast.register(str)
def source_to_ast(source: str, file: str = None) -> ast.Module:
    """
    Return node object for python source.
    """

    if source and not isinstance(source, str):
        raise TypeError('Unexpected type: {}'.format(str(type(source))))

    return _call_with_frames_removed\
                    ( ast.parse
                    , source   = source
                    , filename = file or '<file>'
                    , mode     = 'exec'
                    )


@to_ast.register(types.ModuleType)
def module_to_ast(module: types.ModuleType, file: str = None) -> ast.Module:
    """
    Return node object for python module.
    """

    if module and not isinstance(module, types.ModuleType):
        raise TypeError('Unexpected type: {}'.format(str(type(module))))

    result = None

    try:
        src = inspect.getsource(module)
        file = file or inspect.getfile(module)
        result = source_to_ast(src, file)
    except IOError:
        pass

    return result


@to_ast.register(type)
def class_to_ast(class_: type, file: str = None) -> ast.ClassDef:
    """

    """

    if class_ and not isinstance(class_, type):
        raise TypeError('Unexpected type: {}'.format(str(type(class_))))

    result = None

    try:
        src = inspect.getsource(class_)
        file = file or inspect.getfile(class_)
        result = source_to_ast(src, file)
    except IOError:
        pass

    return result


@to_ast.register(types.MethodType)
def method_to_ast(method: types.MethodType, file: str = None) -> ast.FunctionDef:
    """
    Return node object for method.
    """

    if method and not isinstance(method, types.MethodType):
        raise TypeError('Unexpected type: {}'.format(str(type(method))))

    result = None

    if method and hasattr(method, '__code__'):
        result = code_to_ast(method.__code__, file)

    return result


@to_ast.register(ast.AST)
def node_to_ast(node: ast.AST, file: str = None) -> ast.AST:
    """

    """

    if node and not isinstance(node, ast.AST):
        raise TypeError('Unexpected type: {}'.format(str(type(node))))

    return node

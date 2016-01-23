"""

"""


import ast
import inspect
import types
try:
    from astor.codegen import to_source
except ImportError:
    from codegen import to_source
from .utils import _call_with_frames_removed


__all__ = \
        [ "from_ast"
        , "ast_to_code"
        , "ast_to_func"
        , "ast_to_source"
        , "ast_to_module"
        , "ast_to_node"
        , "ast_to_class"
        , "ast_to_method"
        ]


def ast_to_code(node: ast.AST, old_code: types.CodeType = None, file: str = None) -> types.CodeType:
    """
    Compile node object to code.
    """

    if node and not isinstance(node, ast.AST):
        raise TypeError('Unexpected type for node: {}'.format(str(type(node))))

    if old_code and not isinstance(old_code, types.CodeType):
        raise TypeError('Unexpected type for old_module: {}'.format(str(type(old_code))))

    result = old_code
    if node:
        file = file or (inspect.getfile(old_code) if old_code else None)
        result = _call_with_frames_removed\
                    ( compile
                    , source       = node
                    , filename     = file or '<file>'
                    , mode         = 'exec'
                    , dont_inherit = True
                    )
    elif not old_code:
        raise ValueError('Not specified value')

    return result


def ast_to_module(node: ast.AST, old_module: types.ModuleType = None, file: str = None) -> types.ModuleType:
    """
    Compile node object to module.
    """

    if node and not isinstance(node, ast.AST):
        raise TypeError('Unexpected type for node: {}'.format(str(type(node))))

    if old_module and not isinstance(old_module, types.ModuleType):
        raise TypeError('Unexpected type for old_module: {}'.format(str(type(old_module))))

    if not isinstance(node, ast.Module):
        node = ast.copy_location(ast.Module(body = [node]), node)

    file = file or (inspect.getfile(old_module) if old_module else None)
    code = _call_with_frames_removed\
            ( compile
            , source       = node
            , filename     = file or '<file>'
            , mode         = 'exec'
            , dont_inherit = True
            )
    module = old_module or types.ModuleType()
    exec(code, module.__dict__)

    return module


def ast_to_func(node: ast.AST, old_func: types.FunctionType, file: str = None) -> types.FunctionType:
    """
    Compile node object to function.
    """

    if node and not isinstance(node, (ast.Module, ast.FunctionDef)):
        raise TypeError('Unexpected type for node: {}'.format(str(type(node))))

    if old_func and not isinstance(old_func, types.FunctionType):
        raise TypeError('Unexpected type for old_func: {}'.format(str(type(old_func))))

    result = old_func

    if node and old_func:
        old_code = getattr(old_func, '__code__', None)
        if not isinstance(node, ast.Module):
            mod_node = ast.copy_location(ast.Module(body = [node]), node)
            fun_node = node
        else:
            mod_node = node
            fun_node = node.body[0]
        module = ast_to_code(mod_node, old_code, file=file)
        for code in module.co_consts:
            if not isinstance(code, types.CodeType):
                continue
            if code.co_name == fun_node.name and code.co_firstlineno == fun_node.lineno:
                result.__code__ = code
                break
    else:
        raise ValueError('Not specified value')

    return result


def ast_to_source(node: ast.AST, old_source: str = None, file: str = None) -> str:
    """
    Generate code for node object
    """

    if node and not isinstance(node, ast.AST):
        raise TypeError('Unexpected type for node: {}'.format(str(type(node))))

    if old_source and not isinstance(old_source, str):
        raise TypeError('Unexpected type for old_src: {}'.format(str(type(old_source))))

    return to_source(node) or old_source


def ast_to_class(node: ast.AST, old_class: type = None, file: str = None) -> type:
    """

    :param node:
    :param old_class:
    :param file:
    :return:
    """

    if node and not isinstance(node, (ast.Module, ast.ClassDef)):
        raise TypeError('Unexpected type for node: {}'.format(str(type(node))))

    if old_class and not isinstance(old_class, type):
        raise TypeError('Unexpected type for old_class: {}'.format(str(type(old_class))))

    result = old_class

    # @TODO:
    raise NotImplementedError
    return NotImplemented


def ast_to_method(node: ast.AST, old_method: types.MethodType, file: str = None) -> types.MethodType:
    """

    :param node:
    :param old_method:
    :param file:
    :return:
    """

    raise NotImplementedError
    return NotImplemented


def ast_to_node(node: ast.AST, old_node: ast.AST = None, file: str = None) -> ast.AST:
    """

    """

    if node and not isinstance(node, ast.AST):
        raise TypeError('Unexpected type for node: {}'.format(str(type(node))))

    if old_node and not isinstance(old_node, ast.AST):
        raise TypeError('Unexpected type for old_node: {}'.format(str(type(old_node))))

    return node or old_node


def from_ast(node: ast.AST, old_object, file: str = None):
    """

    :param node:
    :param old_object:
    :return:
    """

    if isinstance(old_object, types.CodeType):
        compiler = ast_to_code
    elif isinstance(old_object, types.ModuleType):
        compiler = ast_to_module
    elif isinstance(old_object, types.FunctionType):
        compiler = ast_to_func
    elif isinstance(old_object, types.MethodType):
        compiler = ast_to_method
    elif isinstance(old_object, str):
        compiler = ast_to_source
    elif isinstance(old_object, type):
        compiler = ast_to_class
    elif isinstance(old_object, ast.AST):
        compiler = ast_to_node
    elif old_object:
        raise TypeError('Unexpected type for node: {}'.format(str(type(node))))
    else:
        raise ValueError('Not specified value')

    result = compiler(node, old_object, file=file)
    return result

"""

"""


from importlib._bootstrap import SourcelessFileLoader, SourceFileLoader, decode_source
from .transform import optimize
from .decompile import source_to_ast
from .compile import ast_to_code


__all__ = \
    [ "activate"
    , "deactivate"
    ]


class Hook(object):
    """

    """

    def __init__(self):
        self._activated = False
        self.activate   = self

    def __call__(self, modules=None, optimizations=None, classes=None, level=None):
        """

        :param modules:
        :param optimizations:
        :param classes:
        :param level:
        :return:
        """

        SourceFileLoader._original_source_to_code = SourceFileLoader.source_to_code
        SourceFileLoader._original_get_code       = SourceFileLoader.get_code
        SourcelessFileLoader._original_get_code   = SourcelessFileLoader.get_code

        # @TODO: handle _optimize
        def _source_to_code(self, data, path, *, _optimize=-1):
            """Return the code object compiled from source.

            The 'data' argument can be any object type that compile() supports.
            """
            src_ = decode_source(data)
            node = source_to_ast(source=src_, file=path)
            node = optimize\
                    ( optimizations = optimizations
                    , classes       = classes
                    , level         = level
                    , value         = node
                    , file          = path
                    )
            code = ast_to_code(node=node, file=path)
            self._opyum_optimized = True
            return code

        def _get_code(self, fullname):
            self._opyum_optimized = False
            code = self._original_get_code(fullname)
            if not self._opyum_optimized:
                code = optimize\
                        ( optimizations = optimizations
                        , classes       = classes
                        , level         = level
                        , value         = code
                        )
            return code

        SourceFileLoader.source_to_code = _source_to_code
        SourceFileLoader.get_code       = _get_code
        SourcelessFileLoader.get_code   = _get_code

        self._activated = True

    def deactivate(self):
        """

        :return:
        """

        if self._activated:

            SourceFileLoader.source_to_code = SourceFileLoader._original_source_to_code
            SourceFileLoader.get_code       = SourceFileLoader._original_get_code
            SourcelessFileLoader.get_code   = SourcelessFileLoader._original_get_code

            del SourceFileLoader._original_source_to_code
            del SourceFileLoader._original_get_code
            del SourcelessFileLoader._original_get_code

            self._activated = False

    def __enter__(self):
        if not self._activated:
            self.activate()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deactivate()

    def __del__(self):
        del self.activate
        self.deactivate()


_hook      = Hook()
activate   = _hook.activate
deactivate = _hook.deactivate

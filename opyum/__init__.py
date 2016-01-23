"""

"""


from .optimizations import \
    ( BasicOptimization
    , ASTOptimization
    , ByteCodeOptimization
    , all_optimizations
    , ast_optimizations
    , bytecode_optimizations
    , install
    , uninstall
    )
from .transform import \
    ( transform
    , optimize
    )
from .hook import \
    ( activate
    , deactivate
    )


__version__ = (0, 1, 0)
__author__  = 'Alexander Marshalov'
__email__   = '_@marshalov.org'
__url__     = 'http://opyum.marshalov.org'
__all__     = \
            [ "BasicOptimization"
            , "ASTOptimization"
            , "ByteCodeOptimization"
            , "transform"
            , "optimize"
            , "activate"
            , "deactivate"
            , "all_optimizations"
            , "ast_optimizations"
            , "bytecode_optimizations"
            , "install"
            , "uninstall"
            ]

"""

"""

import opyum.optimizations
from .optimizations import \
    ( BasicOptimization
    , ASTOptimization
    , ByteCodeOptimization
    # , all_optimizations
    # , ast_optimizations
    # , bytecode_optimizations
    # , install
    # , uninstall
    )
from .transform import \
    ( optimize
    , get_source
    )
from .hook import \
    ( activate
    , deactivate
    )


__version__ = (0, 1, 1)
__author__  = 'Alexander Marshalov'
__email__   = '_@marshalov.org'
__url__     = 'https://github.com/Amper/opyum'
__all__     = \
            [ "optimizations"
            , "BasicOptimization"
            , "ASTOptimization"
            , "ByteCodeOptimization"
            , "optimize"
            , "get_source"
            , "activate"
            , "deactivate"
            # , "all_optimizations"
            # , "ast_optimizations"
            # , "bytecode_optimizations"
            # , "install"
            # , "uninstall"
            ]

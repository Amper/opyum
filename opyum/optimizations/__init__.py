"""

"""


import sys
import os
import pkgutil

from ast import NodeTransformer
from abc import ABCMeta, abstractproperty
from inspect import isabstract
from importlib import import_module

from ..utils import classproperty


__all__ =\
        [ "BasicOptimization"
        , "ASTOptimization"
        , "ByteCodeOptimization"
        , "all_optimizations"
        , "ast_optimizations"
        , "bytecode_optimizations"
        , "install"
        , "uninstall"
        ]


class BasicOptimization(object, metaclass = ABCMeta):
    """

    """

    @classproperty
    def id(cls) -> str:
        """
        :return:
        """
        return cls.__name__

    @abstractproperty
    def name(self) -> str:
        """
        :return: name of optimization
        """
        return NotImplemented

    @abstractproperty
    def description(self) -> str:
       """
        :return: description of optimization
        """
       return NotImplemented

    @abstractproperty
    def level(self) -> int:
        """
        :return: severity level for optimization
        """
        return NotImplemented

    @classproperty
    def optimizations(cls):
        """

        :return:
        """
        if not hasattr(cls, '_optimizations'):
            cls._optimizations = {}
            package = sys.modules[BasicOptimization.__module__]
            path = os.path.dirname(package.__file__)
            for loader, module_name, is_pkg in pkgutil.iter_modules([path]):
                if module_name.startswith('__'):
                    continue
                module = import_module('.' + module_name, package.__name__)
                for _type in vars(module).values():
                    if not isinstance(_type, type):
                        continue
                    if isabstract(_type):
                        continue
                    if not issubclass(_type, cls):
                        continue
                    try:
                        obj = _type()
                        cls._optimizations[obj.id] = obj
                    except:
                        pass
        return cls._optimizations

    @classmethod
    def _check_optimization(cls, optimization):
        if not optimization:
            raise ValueError('Not specified value')
        if isinstance(optimization, type):
            try:
                optimization = optimization()
            except TypeError as exc:
                raise TypeError('Unexpected type for optimization: {}'.format(str(optimization))) from exc
        if not isinstance(optimization, cls):
            raise TypeError('Unexpected type for optimization: {}'.format(str(type(optimization))))
        return optimization

    @classmethod
    def install(cls, optimization):
        """

        """
        optimization = cls._check_optimization(optimization)
        cls.optimizations[optimization.id] = optimization

    @classmethod
    def uninstall(cls, optimization):
        """

        """
        optimization = cls._check_optimization(optimization)
        del cls.optimizations[optimization.id]


class ASTOptimization(BasicOptimization, NodeTransformer):
    """

    """


class ByteCodeOptimization(BasicOptimization):
    """

    """


all_optimizations      = BasicOptimization.optimizations
ast_optimizations      = ASTOptimization.optimizations
bytecode_optimizations = ByteCodeOptimization.optimizations
install                = BasicOptimization.install
uninstall              = BasicOptimization.uninstall






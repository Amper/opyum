"""

"""


__all__ = \
        [ 'classproperty'
        , '_call_with_frames_removed'
        ]


class _ClassPropertyDescriptor(object):
    
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, cls=None):
        if not self.fget:
            raise AttributeError("can't get attribute")
        if cls is None:
            cls = type(obj)
        return self.fget.__get__(obj, cls)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    """

    :param func:
    :return:
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return _ClassPropertyDescriptor(func)


def _call_with_frames_removed(func, *args, **kwds):
    """
    remove_importlib_frames in import.c will always remove sequences
    of importlib frames that end with a call to this function
    Use it instead of a normal call in places where including the importlib
    frames introduces unwanted noise into the traceback (e.g. when executing
    module code)
    """
    return func(*args, **kwds)
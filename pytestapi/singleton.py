import functools
import threading


def singleton(cls):
    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(_cls, *args, **kwargs):
        with threading.Lock():
            it = _cls.__dict__.get('__it__')
            if it is not None:
                return it

            _cls.__it__ = it = _cls.__new_original__(_cls, *args, **kwargs)
            it.__init_original__(*args, **kwargs)
            return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__
    return cls

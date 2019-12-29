import functools

from papurika.service import ServiceMock
from papurika.service import ServiceMockGroup

from typing import Callable


_default_mock = ServiceMockGroup()


####
# shortcuts
####


def activite(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with _default_mock:
            return func(*args, **kwargs)

    return wrapper


add = _default_mock.add


__all__ = ["ServiceMock", "ServiceMockGroup", "activite", "add"]

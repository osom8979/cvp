# -*- coding: utf-8 -*-

from importlib import import_module
from typing import Generic, Tuple, Type, TypeVar, Union

_T = TypeVar("_T")


class ClassPath(Generic[_T]):
    def __init__(self, cls: Union[str, Type[_T]]):
        if isinstance(cls, str):
            module_path, class_name = cls.rsplit(".", 1)
            module = import_module(module_path)
            self._type = getattr(module, class_name)
            self._path = cls
        else:
            self._type = cls
            self._path = cls.__module__ + "." + cls.__name__

    @property
    def type(self) -> Type[_T]:
        return self._type

    @property
    def path(self) -> str:
        return self._path

    def split(self) -> Tuple[str, str]:
        module_path, class_name = self._path.rsplit(".", 1)
        assert isinstance(module_path, str)
        assert isinstance(class_name, str)
        return module_path, class_name

    @property
    def module_path(self) -> str:
        return self.split()[0]

    @property
    def class_name(self) -> str:
        return self.split()[1]

    def __call__(self, *args, **kwargs) -> _T:
        return self._type(*args, **kwargs)

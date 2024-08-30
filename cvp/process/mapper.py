# -*- coding: utf-8 -*-

from typing import Dict, TypeVar

from cvp.process.process import Process
from cvp.process.status import ProcessStatusEx

ProcessT = TypeVar("ProcessT", bound=Process)
KeyT = TypeVar("KeyT")


class ProcessMapper(Dict[KeyT, ProcessT]):
    def spawnable(self, key: KeyT) -> bool:
        return not self.__contains__(key)

    def stoppable(self, key: KeyT) -> bool:
        if self.__contains__(key):
            return self.__getitem__(key).poll() is None
        else:
            return False

    def removable(self, key: KeyT) -> bool:
        if self.__contains__(key):
            return not self.__getitem__(key).is_alive()
        else:
            return False

    def status(self, key: KeyT) -> ProcessStatusEx:
        if self.__contains__(key):
            return self.__getitem__(key).status()
        else:
            return ProcessStatusEx.not_exists

    def interrupt(self, key: KeyT) -> None:
        self.__getitem__(key).interrupt()

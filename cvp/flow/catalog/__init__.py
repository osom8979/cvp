# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Dict

from cvp.flow.catalog import events
from cvp.flow.node import FlowNode
from cvp.inspect.member import is_dunder, is_sunder


@lru_cache
def builtin_catalog_submodules():
    return [events]


class FlowCatalog(Dict[str, FlowNode]):
    @classmethod
    def from_builtins(cls):
        result = cls()

        for module in builtin_catalog_submodules():
            for key in dir(module):
                # Naming filters
                if is_dunder(key):
                    continue
                if is_sunder(key):
                    continue

                o = getattr(events, key)

                # Typing filters
                if not isinstance(o, type):
                    continue
                if not issubclass(o, FlowNode):
                    continue

                result[o.__name__] = o()

        return result

# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Dict, Union

from cvp.flow.catalog import events
from cvp.flow.datas.templates.node import NodeTemplate
from cvp.flow.path import FlowPath
from cvp.inspect.member import is_dunder, is_sunder


@lru_cache
def builtin_catalog_submodules():
    return [events]


class Nodes(Dict[str, NodeTemplate]):
    pass


class FlowCatalog(Dict[str, Nodes]):
    @classmethod
    def from_builtins(cls):
        result = cls()

        for module in builtin_catalog_submodules():
            module_path = module.__name__
            nodes = Nodes()

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
                if not issubclass(o, NodeTemplate):
                    continue

                node_name = o.__name__
                nodes[node_name] = o()

            result[module_path] = nodes

        return result

    def get_node_template(self, path: Union[str, FlowPath]) -> NodeTemplate:
        if not isinstance(path, FlowPath):
            if not isinstance(path, str):
                raise TypeError(f"Unsupported path type: {type(path).__name__}")
            path = FlowPath(path)

        assert isinstance(path, FlowPath)
        split_result = path.split()
        module_path = split_result.module
        node_name = split_result.node
        return self.__getitem__(module_path).__getitem__(node_name)

# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Iterable, List, Optional, TypeGuard, Union

from cvp.flow.datas.arc import Arc
from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin

SelectableAny = Union[Node, Pin, Arc]


class SelectedItems:
    _items: OrderedDict[int, SelectableAny]

    def __init__(self):
        self._items = OrderedDict()

    def __len__(self):
        return len(self._items)

    def keys(self):
        return self._items.keys()

    def values(self):
        return self._items.values()

    def items(self):
        return self._items.items()

    @staticmethod
    def _is_node(item: SelectableAny) -> TypeGuard[Node]:
        return isinstance(item, Node)

    @staticmethod
    def _is_pin(item: SelectableAny) -> TypeGuard[Pin]:
        return isinstance(item, Pin)

    @staticmethod
    def _is_arc(item: SelectableAny) -> TypeGuard[Arc]:
        return isinstance(item, Arc)

    @property
    def nodes(self) -> List[Node]:
        return list(filter(self._is_node, self._items.values()))

    @property
    def pins(self) -> List[Pin]:
        return list(filter(self._is_pin, self._items.values()))

    @property
    def arcs(self) -> List[Arc]:
        return list(filter(self._is_arc, self._items.values()))

    @property
    def selected_node_only(self) -> Optional[Node]:
        if 1 != len(self._items):
            return None
        first_item = next(iter(self._items.values()))
        if isinstance(first_item, Node):
            return first_item
        else:
            return None

    @property
    def selected_pin_only(self) -> Optional[Pin]:
        if 1 != len(self._items):
            return None
        first_item = next(iter(self._items.values()))
        if isinstance(first_item, Pin):
            return first_item
        else:
            return None

    @property
    def selected_arc_only(self) -> Optional[Arc]:
        if 1 != len(self._items):
            return None
        first_item = next(iter(self._items.values()))
        if isinstance(first_item, Arc):
            return first_item
        else:
            return None

    def clear(self) -> None:
        self._items.clear()

    def extends(self, items: Iterable[SelectableAny]) -> None:
        for item in items:
            self._items[id(item)] = item

    def add(self, item: SelectableAny) -> None:
        if not item.selected:
            raise ValueError("Item must be selected")

        self._items[id(item)] = item

    def remove(self, item: SelectableAny) -> None:
        if item.selected:
            raise ValueError("Items must be unselected")

        try:
            self._items.pop(id(item))
        except KeyError:
            pass

    def apply(self, item: SelectableAny) -> None:
        if item.selected:
            self.add(item)
        else:
            self.remove(item)

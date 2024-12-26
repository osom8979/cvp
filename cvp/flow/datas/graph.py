# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Set, Union
from uuid import uuid4

from cvp.flow.datas.action import Action
from cvp.flow.datas.arc import Arc
from cvp.flow.datas.axis import Axis
from cvp.flow.datas.canvas import Canvas
from cvp.flow.datas.connect_pair import ConnectPair
from cvp.flow.datas.constants import DEFAULT_GRAPH_COLOR, EMPTY_TEXT
from cvp.flow.datas.dtype import DataType
from cvp.flow.datas.grid import Grid
from cvp.flow.datas.node import Node
from cvp.flow.datas.node_pin import NodePin
from cvp.flow.datas.stream import Stream
from cvp.flow.datas.style import Style
from cvp.types.colors import RGBA
from cvp.types.shapes import Size


@dataclass
class Graph:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = EMPTY_TEXT
    docs: str = EMPTY_TEXT
    color: RGBA = DEFAULT_GRAPH_COLOR
    nodes: List[Node] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    dtypes: List[DataType] = field(default_factory=list)
    canvas: Canvas = field(default_factory=Canvas)
    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)
    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)
    style: Style = field(default_factory=Style)

    def clear_state(self) -> None:
        for node in self.nodes:
            node.hovering = False
            # Do not change the `node.selected` property.
            for pin in node.pins:
                pin.hovering = False
                pin.connectable = False

    def find_hovering_node(self) -> Optional[Node]:
        for node in self.nodes:
            if node.hovering:
                return node
        return None

    def find_hovering_pin(self, node: Optional[Node] = None) -> Optional[NodePin]:
        if node is None:
            node = self.find_hovering_node()
            if node is None:
                return None

        if not node.hovering:
            raise ValueError("Only hovering nodes are allowed")

        pin = node.find_hovering_pin()
        if pin is None:
            return None

        return NodePin(node, pin)

    def find_arc(self, uuid: str) -> Optional[Arc]:
        for arc in self.arcs:
            if arc.uuid == uuid:
                return arc
        return None

    def pop_arcs(self, uuids: Union[Set[str], Sequence[str]]) -> List[Arc]:
        if not isinstance(uuids, set):
            uuids = set(uuids)
        remain_arcs = list()
        pop_arcs = list()
        for arc in self.arcs:
            if arc.uuid in uuids:
                pop_arcs.append(arc)
            else:
                remain_arcs.append(arc)
        self.arcs.clear()
        self.arcs.extend(remain_arcs)
        return pop_arcs

    def find_selected_arcs(self) -> List[Arc]:
        result = list()
        for arc in self.arcs:
            if arc.selected:
                result.append(arc)
        return result

    def find_selected_nodes(self) -> List[Node]:
        result = list()
        for node in self.nodes:
            if node.selected:
                result.append(node)
        return result

    def select_all_nodes(self) -> None:
        for node in self.nodes:
            node.selected = True

    def unselect_all_nodes(self) -> None:
        for node in self.nodes:
            node.selected = False

    def select_on_hovering_nodes(self) -> None:
        for node in self.nodes:
            node.selected = node.hovering

    def flip_selected_on_hovering_nodes(self) -> None:
        for node in self.nodes:
            if node.hovering:
                node.selected = not node.selected

    def move_on_selected_nodes(self, delta: Size) -> None:
        dx, dy = delta
        for node in self.nodes:
            if not node.selected:
                continue
            x, y = node.node_pos
            node.node_pos = x + dx, y + dy

    @staticmethod
    def reorder_connectable_pins(left: NodePin, right: NodePin) -> ConnectPair:
        if left.node == right.node:
            raise ValueError("Identical nodes cannot be connected")
        if left.pin.stream == right.pin.stream:
            raise ValueError("Identical streams cannot be connected")
        if left.pin.action != right.pin.action:
            raise ValueError("The action of the pins must match")
        if left.pin.dtype != right.pin.dtype:
            raise ValueError("The dtype of the pins must match")

        if left.pin.stream == Stream.input:
            assert right.pin.stream == Stream.output
            out_conn = right
            in_conn = left
        else:
            assert left.pin.stream == Stream.output
            assert right.pin.stream == Stream.input
            out_conn = left
            in_conn = right

        out_pin = out_conn.pin
        in_pin = in_conn.pin
        assert out_pin.stream == Stream.output
        assert in_pin.stream == Stream.input
        assert out_pin.action == in_pin.action
        action = in_pin.action

        if action == Action.flow and out_pin.arcs:
            raise ValueError("There cannot be multiple output flow pins")
        if action == Action.data and in_pin.arcs:
            raise ValueError("There cannot be multiple input data pins")

        return ConnectPair(out_conn, in_conn)

    @staticmethod
    def is_connectable_pins(left: NodePin, right: NodePin) -> bool:
        try:
            Graph.reorder_connectable_pins(left, right)
        except ValueError:
            return False
        else:
            return True

    def connect_pins(
        self,
        out_conn: NodePin,
        in_conn: NodePin,
        *,
        no_reorder=False,
    ) -> Arc:
        if not no_reorder:
            out_conn, in_conn = self.reorder_connectable_pins(out_conn, in_conn)

        arc = Arc()
        arc.output = out_conn
        arc.input = in_conn

        self.arcs.append(arc)
        out_conn.pin.arcs.append(arc.uuid)
        in_conn.pin.arcs.append(arc.uuid)

        return arc

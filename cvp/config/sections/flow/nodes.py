# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.shapes import Size
from cvp.variables import FLOW_NODES_ITEM_SPACING, FLOW_NODES_SHOW_LAYOUT


@dataclass
class Nodes:
    show_layout: bool = FLOW_NODES_SHOW_LAYOUT
    item_spacing: Size = FLOW_NODES_ITEM_SPACING

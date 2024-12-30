# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.flow.datas.constants import (
    DATA_PIN_N_ICON,
    DATA_PIN_Y_ICON,
    DEFAULT_ITEM_SPACING,
    FLOW_PIN_N_ICON,
    FLOW_PIN_Y_ICON,
)
from cvp.flow.datas.size import FontSize
from cvp.flow.datas.stroke import Stroke
from cvp.palette.basic import BLACK, BLUE, RED, SILVER
from cvp.palette.tableau import ORANGE
from cvp.types.colors import RGBA
from cvp.types.shapes import Size
from cvp.variables import DEFAULT_CURVE_TESSELLATION_TOL


@dataclass
class Style:
    selected_node: Stroke = field(default_factory=lambda: Stroke.default_selected())
    hovering_node: Stroke = field(default_factory=lambda: Stroke.default_hovering())
    normal_node: Stroke = field(default_factory=lambda: Stroke.default_normal())

    normal_color: RGBA = field(default_factory=lambda: (*BLACK, 0.8))
    hovering_color: RGBA = field(default_factory=lambda: (*ORANGE, 0.9))
    select_color: RGBA = field(default_factory=lambda: (*RED, 0.9))
    layout_color: RGBA = field(default_factory=lambda: (*RED, 0.8))

    pin_connection_color: RGBA = field(default_factory=lambda: (*RED, 0.8))
    pin_connection_thickness: float = 2.0

    selection_box_color: RGBA = field(default_factory=lambda: (*BLUE, 0.3))
    selection_box_thickness: float = 1.0

    arc_color: RGBA = field(default_factory=lambda: (*SILVER, 0.8))
    arc_thickness: float = 2.0
    arc_anchor_size: float = 4.0

    bezier_curve_tess_tol: float = DEFAULT_CURVE_TESSELLATION_TOL

    item_spacing: Size = DEFAULT_ITEM_SPACING

    emblem_size: FontSize = FontSize.large
    title_size: FontSize = FontSize.medium
    text_size: FontSize = FontSize.normal
    icon_size: FontSize = FontSize.normal

    flow_pin_n_icon: str = FLOW_PIN_N_ICON
    flow_pin_y_icon: str = FLOW_PIN_Y_ICON
    data_pin_n_icon: str = DATA_PIN_N_ICON
    data_pin_y_icon: str = DATA_PIN_Y_ICON

    show_layout: bool = False

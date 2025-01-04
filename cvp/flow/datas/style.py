# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Final

from cvp.flow.datas.stroke import Stroke
from cvp.fonts.scale import FontScale
from cvp.palette.basic import BLACK, BLUE, RED, SILVER, WHITE
from cvp.palette.tableau import ORANGE
from cvp.types.colors import RGBA
from cvp.types.shapes import Size
from cvp.variables import BEZIER_CURVE_TESSELLATION_TOL

DEFAULT_ITEM_SPACING: Final[Size] = 2.0, 2.0


@dataclass
class Style:
    selected_node: Stroke = field(default_factory=lambda: Stroke.default_selected())
    hovering_node: Stroke = field(default_factory=lambda: Stroke.default_hovering())
    normal_node: Stroke = field(default_factory=lambda: Stroke.default_normal())

    normal_color: RGBA = field(default_factory=lambda: (*BLACK, 0.8))
    hovering_color: RGBA = field(default_factory=lambda: (*ORANGE, 0.9))
    select_color: RGBA = field(default_factory=lambda: (*RED, 0.9))
    layout_color: RGBA = field(default_factory=lambda: (*RED, 0.8))

    node_bg_color: RGBA = field(default_factory=lambda: (*WHITE, 0.6))

    pin_connection_color: RGBA = field(default_factory=lambda: (*RED, 0.8))
    pin_connection_thickness: float = 2.0

    selection_box_color: RGBA = field(default_factory=lambda: (*BLUE, 0.3))
    selection_box_thickness: float = 1.0

    arc_color: RGBA = field(default_factory=lambda: (*SILVER, 0.8))
    arc_thickness: float = 2.0

    anchor_color: RGBA = field(default_factory=lambda: (*BLUE, 0.8))
    anchor_radius: float = 3.0

    bezier_curve_tess_tol: float = BEZIER_CURVE_TESSELLATION_TOL

    item_spacing: Size = DEFAULT_ITEM_SPACING

    icon_scale: FontScale = FontScale.large
    title_scale: FontScale = FontScale.medium
    text_scale: FontScale = FontScale.normal
    pin_scale: FontScale = FontScale.normal

    show_layout: bool = False

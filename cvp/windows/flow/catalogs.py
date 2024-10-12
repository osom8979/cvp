# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.flow.path import PATH_SEPARATOR
from cvp.imgui.drag_type import DRAG_FLOW_NODE_TYPE as _DRAG_TYPE
from cvp.types import override
from cvp.widgets.widget import WidgetInterface


class Catalogs(WidgetInterface):
    def __init__(self, context: Context):
        self._context = context

    @override
    def on_process(self) -> None:
        imgui.text("Catalogs:")

        for module_path, nodes in self._context.fm.catalog.items():
            module_name = module_path.split(PATH_SEPARATOR)[-1]
            imgui.push_id(module_path)
            try:
                expanded, visible = imgui.collapsing_header(module_name)
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(module_path)

                if expanded:
                    imgui.set_cursor_pos_x(imgui.get_tree_node_to_label_spacing())

                    for node_name, node_template in nodes.items():
                        imgui.selectable(node_name)

                        if not self._context.fm.cursored:
                            continue

                        with imgui.begin_drag_drop_source() as drag_drop_src:
                            if drag_drop_src.dragging:
                                node_name = node_template.name
                                node_path = module_path + PATH_SEPARATOR + node_name
                                node_data = node_path.encode()

                                imgui.set_drag_drop_payload(_DRAG_TYPE, node_data)
                                imgui.text(node_name)
            finally:
                imgui.pop_id()

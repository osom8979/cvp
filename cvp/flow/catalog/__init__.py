# -*- coding: utf-8 -*-

from typing import Dict

from cvp.flow.node import FlowNode


class FlowCategory(Dict[str, FlowNode]):
    pass


class FlowCatalog(Dict[str, FlowCategory]):
    pass

# -*- coding: utf-8 -*-

from typing import Dict

from cvp.flow.node import FlowNodeTemplate


class FlowCategory(Dict[str, FlowNodeTemplate]):
    pass


class FlowCatalog(Dict[str, FlowCategory]):
    pass

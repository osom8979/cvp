# -*- coding: utf-8 -*-

from typing import Dict

from cvp.flow.template import FlowTemplate


class FlowCategory(Dict[str, FlowTemplate]):
    pass


class FlowCatalog(Dict[str, FlowCategory]):
    pass

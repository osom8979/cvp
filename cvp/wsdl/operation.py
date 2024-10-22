# -*- coding: utf-8 -*-

from typing import List, Tuple

from zeep.wsdl.definitions import Operation
from zeep.xsd import Element


class BindOperation:
    def __init__(self, operation: Operation):
        self.operation = operation

    @property
    def input_elements(self) -> List[Tuple[str, Element]]:
        try:
            return self.operation.input.body.type.elements
        except AttributeError:
            return list()

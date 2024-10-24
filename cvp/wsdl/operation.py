# -*- coding: utf-8 -*-

from typing import Any, List, Tuple

from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsdl.definitions import Operation
from zeep.xsd import Element

from cvp.inspect.argument import Argument, BindArguments
from cvp.resources.subdirs.pickles import Pickles
from cvp.types import override


class WsdlOperationProxy(OperationProxy):
    def __init__(
        self,
        pickles: Pickles,
        uuid: str,
        binding_name: str,
        operation_name: str,
        service_proxy: ServiceProxy,
        operation: Operation,
    ):
        super().__init__(service_proxy, operation_name)
        self._uuid = uuid
        self._pickles = pickles
        self._binding_name = binding_name
        self._operation = operation
        self._arguments = self._create_arguments()

    def _create_arguments(self):
        result = BindArguments()
        for name, element in self.input_elements:
            result[name] = Argument.from_details(name)
        return result

    @property
    def input_elements(self) -> List[Tuple[str, Element]]:
        try:
            return self._operation.input.body.type.elements
        except AttributeError:
            return list()

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        assert isinstance(self._op_name, str)
        return self._uuid, self._binding_name, self._op_name

    def has_cache(self) -> bool:
        return self._pickles.has_object(*self.cache_args)

    def read_cache(self) -> Any:
        return self._pickles.read_object(*self.cache_args)

    def write_cache(self, o: Any) -> int:
        return self._pickles.write_object(o, *self.cache_args)

    @override
    def __call__(self, *args, **kwargs):
        if self.has_cache():
            return self.read_cache()
        else:
            response = super().__call__(*args, **kwargs)
            self.write_cache(response)
            return response

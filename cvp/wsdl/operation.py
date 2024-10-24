# -*- coding: utf-8 -*-

from typing import Any, List, Optional, Tuple

from zeep.client import Factory
from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsdl.definitions import Operation
from zeep.xsd import Element

from cvp.inspect.argument import Argument, ArgumentMapper
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
        factory: Optional[Factory] = None,
    ):
        super().__init__(service_proxy, operation_name)
        self._uuid = uuid
        self._pickles = pickles
        self._binding_name = binding_name
        self._operation = operation
        self._arguments = self._create_arguments(factory)

    def _create_arguments(self, factory: Optional[Factory] = None):
        result = ArgumentMapper()
        for name, element in self.input_elements:
            result[name] = Argument.from_details(name)
            if factory is not None:
                pass
        return result

    @property
    def input_elements(self) -> List[Tuple[str, Element]]:
        try:
            return self._operation.input.body.type.elements
        except AttributeError:
            return list()

    @property
    def arguments(self):
        return self._arguments

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def binding_name(self) -> str:
        return self._binding_name

    @property
    def name(self) -> str:
        assert isinstance(self._op_name, str)
        return self._op_name

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        return self.uuid, self.binding_name, self.name

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

    def call_with_arguments(self):
        return self.__call__(**self._arguments.kwargs())

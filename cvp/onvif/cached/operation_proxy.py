# -*- coding: utf-8 -*-

from typing import Any, List, Tuple

from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsdl.definitions import Operation
from zeep.xsd import Element

from cvp.config.sections.onvif import OnvifConfig
from cvp.resources.home import HomeDir
from cvp.types import override


class OnvifCachedOperationProxy(OperationProxy):
    def __init__(
        self,
        onvif_config: OnvifConfig,
        home: HomeDir,
        binding_name: str,
        service_proxy: ServiceProxy,
        operation_name: str,
        operation: Operation,
    ):
        super().__init__(service_proxy, operation_name)
        self._onvif_config = onvif_config
        self._home = home
        self._binding_name = binding_name
        self._operation = operation

    @property
    def input_elements(self) -> List[Tuple[str, Element]]:
        try:
            return self._operation.input.body.type.elements
        except AttributeError:
            return list()

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        assert isinstance(self._op_name, str)
        return self._onvif_config.uuid, self._binding_name, self._op_name

    def has_cache(self) -> bool:
        return self._home.onvifs.has_onvif_object(*self.cache_args)

    def read_cache(self) -> Any:
        return self._home.onvifs.read_onvif_object(*self.cache_args)

    def write_cache(self, o: Any) -> int:
        return self._home.onvifs.write_onvif_object(*self.cache_args, o)

    @override
    def __call__(self, *args, **kwargs):
        if self.has_cache():
            return self.read_cache()
        else:
            response = super().__call__(*args, **kwargs)
            self.write_cache(response)
            return response

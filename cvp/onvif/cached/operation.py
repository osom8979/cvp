# -*- coding: utf-8 -*-

from typing import Any

from zeep.proxy import OperationProxy, ServiceProxy

from cvp.config.sections.onvif import OnvifConfig
from cvp.resources.home import HomeDir
from cvp.types import override


class CachedOperationProxy(OperationProxy):
    def __init__(
        self,
        onvif_config: OnvifConfig,
        home: HomeDir,
        binding: str,
        service_proxy: ServiceProxy,
        operation_name: str,
    ):
        super().__init__(service_proxy, operation_name)
        self._onvif_config = onvif_config
        self._home = home
        self._binding = binding

    @property
    def uuid(self):
        return self._onvif_config.uuid

    @property
    def binding(self):
        return self._binding

    @property
    def docs(self) -> str:
        return super().__doc__()

    @property
    def api(self):
        return self._op_name

    @property
    def onvifs_path(self):
        return self._home.onvifs

    def has_cache(self) -> bool:
        return self.onvifs_path.has_onvif_object(self.uuid, self.binding, self.api)

    def read_cache(self) -> Any:
        return self.onvifs_path.read_onvif_object(self.uuid, self.binding, self.api)

    def write_cache(self, o: Any) -> int:
        return self.onvifs_path.write_onvif_object(self.uuid, self.binding, self.api, o)

    @override
    def __call__(self, *args, **kwargs):
        if self.has_cache():
            return self.read_cache()
        else:
            response = super().__call__(*args, **kwargs)
            self.write_cache(response)
            return response

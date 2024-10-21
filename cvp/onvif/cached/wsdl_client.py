# -*- coding: utf-8 -*-

from typing import Optional

from zeep import Transport
from zeep.wsse import UsernameToken

from cvp.config.sections.onvif import OnvifConfig
from cvp.onvif.cached.operation_proxy import OnvifCachedOperationProxy
from cvp.resources.home import HomeDir
from cvp.wsdl.client import WsdlClient
from cvp.wsdl.declaration import WsdlDeclaration


class OnvifCachedWsdlClient(WsdlClient):
    def __init__(
        self,
        onvif_config: OnvifConfig,
        home: HomeDir,
        declaration: WsdlDeclaration,
        wsse: Optional[UsernameToken] = None,
        transport: Optional[Transport] = None,
        address: Optional[str] = None,
    ):
        super().__init__(declaration, wsse, transport, address)
        self._onvif_config = onvif_config
        self._home = home
        self._reallocate_onvif_cached_operation_proxies()

    def _reallocate_onvif_cached_operation_proxies(self):
        self._service._operations = self._create_onvif_cached_operation_proxies()

    def _create_onvif_cached_operation_proxies(self):
        result = dict()
        for name, operation in self.binding_operations.items():
            result[name] = OnvifCachedOperationProxy(
                onvif_config=self._onvif_config,
                home=self._home,
                binding_name=self._declaration.binding,
                service_proxy=self._service,
                operation_name=name,
                operation=operation,
            )
        return result

    def update_onvif_ns_prefixes(self):
        self.client.set_ns_prefix("tds", "http://www.onvif.org/ver10/device/wsdl")
        self.client.set_ns_prefix("tev", "http://www.onvif.org/ver10/events/wsdl")
        self.client.set_ns_prefix("timg", "http://www.onvif.org/ver20/imaging/wsdl")
        self.client.set_ns_prefix("tmd", "http://www.onvif.org/ver10/deviceIO/wsdl")
        self.client.set_ns_prefix("tptz", "http://www.onvif.org/ver20/ptz/wsdl")
        self.client.set_ns_prefix("ttr", "http://www.onvif.org/ver10/media/wsdl")
        self.client.set_ns_prefix("ter", "http://www.onvif.org/ver10/error")

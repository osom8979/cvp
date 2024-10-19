# -*- coding: utf-8 -*-

from cvp.onvif.cache import onvif_api
from cvp.onvif.types import (
    GetDeviceInformationResponse,
    GetServicesResponse,
    GetSystemDateAndTimeResponse,
)
from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifDeviceManagement(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver10/device/wsdl",
        wsdl="http://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl",
        binding="DeviceBinding",
    )

    @onvif_api
    def get_capabilities(self):
        """
        This method has been replaced by the more generic GetServices method.
        For capabilities of individual services refer to the GetServiceCapabilities
        methods.
        """
        return self.service.GetCapabilities()

    @onvif_api
    def get_system_date_and_time(self) -> GetSystemDateAndTimeResponse:
        return self.service.GetSystemDateAndTime()

    @onvif_api
    def get_device_information(self) -> GetDeviceInformationResponse:
        return self.service.GetDeviceInformation()

    @onvif_api
    def get_services(self, include_capability=False) -> GetServicesResponse:
        return self.service.GetServices(IncludeCapability=include_capability)

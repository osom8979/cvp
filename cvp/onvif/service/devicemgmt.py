# -*- coding: utf-8 -*-

from cvp.onvif.types import (
    GetDeviceInformationResponse,
    GetServicesResponse,
    GetSystemDateAndTimeResponse,
)
from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifDeviceManagement(WsdlService):
    """
    http://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl
    """

    __wsdl_declaration__ = WsdlDeclaration(
        declaration="http://www.onvif.org/ver10/device/wsdl",
        http_sub="device_service",
        wsdl_file="devicemgmt.wsdl",
        subclass="DeviceManagement",
        binding_names=["DeviceBinding"],
    )

    def get_capabilities(self):
        """
        This method has been replaced by the more generic GetServices method.
        For capabilities of individual services refer to the GetServiceCapabilities
        methods.
        """
        return self.service.GetCapabilities()

    def get_system_date_and_time(self) -> GetSystemDateAndTimeResponse:
        return self.service.GetSystemDateAndTime()

    def get_device_information(self) -> GetDeviceInformationResponse:
        return self.service.GetDeviceInformation()

    def get_services(self, include_capability=False) -> GetServicesResponse:
        return self.service.GetServices(IncludeCapability=include_capability)

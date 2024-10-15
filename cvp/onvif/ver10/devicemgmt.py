# -*- coding: utf-8 -*-

from typing import Optional

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.onvif.service import OnvifService
from cvp.resources.home import HomeDir
from cvp.wsdl.declaration import WsdlDeclaration

ONVIF_DECL_DEVICE_MANAGEMENT = WsdlDeclaration(
    declaration="http://www.onvif.org/ver10/device/wsdl",
    http_sub="device_service",
    wsdl_file="devicemgmt.wsdl",
    subclass="DeviceManagement",
    binding_names=["DeviceBinding"],
)


class OnvifDeviceManagement(OnvifService):
    """
    http://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl
    """

    def __init__(
        self,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
        password: Optional[str] = None,
    ):
        super().__init__(
            decl=ONVIF_DECL_DEVICE_MANAGEMENT,
            onvif_config=onvif_config,
            wsdl_config=wsdl_config,
            home=home,
            password=password,
        )

    def get_system_date_and_time(self):
        return self.service.GetSystemDateAndTime()

    def get_capabilities(self):
        """
        This method has been replaced by the more generic GetServices method.
        For capabilities of individual services refer to the GetServiceCapabilities
        methods.
        """
        return self.service.GetCapabilities()

    def get_services(self, include_capability=False):
        return self.service.GetServices(IncludeCapability=include_capability)

    def get_device_information(self):
        return self.service.GetDeviceInformation()

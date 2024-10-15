# -*- coding: utf-8 -*-

from typing import Optional

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.onvif.service import OnvifService
from cvp.resources.home import HomeDir
from cvp.wsdl.declaration import WsdlDeclaration

ONVIF_DECL_DEVICE_IO = WsdlDeclaration(
    declaration="http://www.onvif.org/ver10/deviceIO/wsdl",
    http_sub="DeviceIO",
    wsdl_file="deviceio.wsdl",
    subclass="DeviceIO",
)


class OnvifDeviceIO(OnvifService):
    def __init__(
        self,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
        password: Optional[str] = None,
    ):
        super().__init__(
            decl=ONVIF_DECL_DEVICE_IO,
            onvif_config=onvif_config,
            wsdl_config=wsdl_config,
            home=home,
            password=password,
        )

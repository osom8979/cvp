# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifDeviceIO(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        declaration="http://www.onvif.org/ver10/deviceIO/wsdl",
        http_sub="DeviceIO",
        wsdl_file="deviceio.wsdl",
        subclass="DeviceIO",
    )

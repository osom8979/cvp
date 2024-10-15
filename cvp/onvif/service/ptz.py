# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifPTZ(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        declaration="http://www.onvif.org/ver20/ptz/wsdl",
        http_sub="PTZ",
        wsdl_file="ptz.wsdl",
        subclass="PTZ",
        binding_names=["PTZBinding"],
    )

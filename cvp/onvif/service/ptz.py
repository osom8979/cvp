# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifPTZ(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver20/ptz/wsdl",
        wsdl="http://www.onvif.org/ver20/ptz/wsdl/ptz.wsdl",
        binding="PTZBinding",
    )

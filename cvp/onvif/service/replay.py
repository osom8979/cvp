# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifReplay(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver10/replay/wsdl",
        wsdl="http://www.onvif.org/ver10/replay.wsdl",
        binding="ReplayBinding",
    )

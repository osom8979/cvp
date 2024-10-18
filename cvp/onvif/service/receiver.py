# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifReceiver(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver10/receiver/wsdl",
        wsdl="http://www.onvif.org/ver10/receiver.wsdl",
        binding="ReceiverBinding",
    )

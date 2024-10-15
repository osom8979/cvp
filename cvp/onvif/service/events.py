# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifEvents(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        declaration="http://www.onvif.org/ver10/events/wsdl",
        http_sub="Events",
        wsdl_file="events.wsdl",
        subclass="Events",
    )

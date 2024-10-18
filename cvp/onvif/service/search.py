# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifSearch(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver10/search/wsdl",
        wsdl="http://www.onvif.org/ver10/search.wsdl",
        binding="SearchBinding",
    )

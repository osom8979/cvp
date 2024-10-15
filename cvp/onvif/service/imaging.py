# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifImaging(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        declaration="http://www.onvif.org/ver20/imaging/wsdl",
        http_sub="Imaging",
        wsdl_file="imaging.wsdl",
        subclass="Imaging",
        binding_names=["ImagingBinding"],
    )

# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifImaging(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver20/imaging/wsdl",
        wsdl="http://www.onvif.org/ver20/imaging/wsdl/imaging.wsdl",
        binding="ImagingBinding",
    )

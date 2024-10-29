# -*- coding: utf-8 -*-

from typing import Final

from cvp.wsdl.cache import ZeepFileCache
from cvp.wsdl.schema import XsdSchema
from cvp.wsdl.transport import create_transport_with_package_asset

ONVIF_XSD_LOCATION: Final[str] = "http://www.onvif.org/ver10/schema/onvif.xsd"


class OnvifSchema(XsdSchema):
    def __init__(self, location=ONVIF_XSD_LOCATION):
        transport = create_transport_with_package_asset()
        assert isinstance(transport.cache, ZeepFileCache)
        super().__init__(location=location, transport=transport)

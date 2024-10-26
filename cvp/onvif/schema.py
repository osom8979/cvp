# -*- coding: utf-8 -*-

from typing import Final, List

from cvp.wsdl.cache import ZeepFileCache
from cvp.wsdl.schema import XsdSchema
from cvp.wsdl.transport import create_transport_with_package_asset

ONVIF_XSD: Final[str] = "http://www.onvif.org/ver10/schema/onvif.xsd"
ONVIF_NAMESPACE: Final[str] = "http://www.onvif.org/ver10/schema/"

xs: Final[str] = "xs"
XSD_URL: Final[str] = "http://www.w3.org/2001/XMLSchema"


class OnvifSchema(XsdSchema):
    def __init__(self, location=ONVIF_XSD):
        self._xs = {xs: XSD_URL}
        transport = create_transport_with_package_asset()
        assert isinstance(transport.cache, ZeepFileCache)
        super().__init__(location=location, transport=transport)

    @property
    def simple_types(self):
        return self.root.xpath(f"//{xs}:simpleType", namespaces={xs: XSD_URL})

    @property
    def complex_types(self):
        return self.root.xpath(f"//{xs}:complexType", namespaces={xs: XSD_URL})

    @property
    def simple_type_names(self):
        return [e.get("name") for e in self.simple_types]

    @property
    def complex_type_names(self):
        return [e.get("name") for e in self.complex_types]

    def get_enumerations(self, simple_type: str) -> List[str]:
        xpath = f"//xs:simpleType[@name='{simple_type}']/xs:restriction/xs:enumeration"
        enumerations = self.root.xpath(xpath, namespaces={"xs": XSD_URL})
        return [enum.get("value") for enum in enumerations]

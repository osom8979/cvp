# -*- coding: utf-8 -*-

from typing import Final, List

from lxml import etree

from cvp.wsdl.cache import ZeepFileCache
from cvp.wsdl.transport import create_transport_with_package_asset

ONVIF_XSD: Final[str] = "http://www.onvif.org/ver10/schema/onvif.xsd"


class OnvifSchema:
    def __init__(self, location=ONVIF_XSD):
        transport = create_transport_with_package_asset()
        assert isinstance(transport.cache, ZeepFileCache)

        onvif_data = transport.cache.get(location)
        assert onvif_data is not None

        self._element = etree.XML(onvif_data)
        assert self._element is not None

        self._xs = {"xs": "http://www.w3.org/2001/XMLSchema"}

    @property
    def element(self):
        return self._element

    def xpath(self, xpath: str):
        return self._element.xpath(xpath, namespaces=self._xs)

    @property
    def simple_types(self):
        return self.xpath("//xs:simpleType")

    @property
    def complex_types(self):
        return self.xpath("//xs:complexType")

    @property
    def simple_type_names(self):
        return [e.get("name") for e in self.simple_types]

    @property
    def complex_type_names(self):
        return [e.get("name") for e in self.complex_types]

    def get_enumerations(self, simple_type: str) -> List[str]:
        xpath = f"//xs:simpleType[@name='{simple_type}']/xs:restriction/xs:enumeration"
        enumerations = self.xpath(xpath)
        return [enum.get("value") for enum in enumerations]

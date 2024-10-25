# -*- coding: utf-8 -*-

from typing import Final

from zeep.xsd.schema import Schema

from cvp.wsdl.transport import create_transport_with_package_asset

COMMON_XSD: Final[str] = "http://www.onvif.org/ver10/schema/common.xsd"
METADATASTREAM_XSD: Final[str] = "http://www.onvif.org/ver10/schema/metadatastream.xsd"
ONVIF_XSD: Final[str] = "http://www.onvif.org/ver10/schema/onvif.xsd"


class OnvifSchema:
    def __init__(
        self,
        common=COMMON_XSD,
        metadatastream=METADATASTREAM_XSD,
        onvif=ONVIF_XSD,
    ):
        transport = create_transport_with_package_asset()
        self._common = Schema(transport=transport, location=common)
        self._metadatastream = Schema(transport=transport, location=metadatastream)
        self._onvif = Schema(transport=transport, location=onvif)

    @property
    def common(self):
        return self._common

    @property
    def metadatastream(self):
        return self._metadatastream

    @property
    def onvif(self):
        return self._onvif

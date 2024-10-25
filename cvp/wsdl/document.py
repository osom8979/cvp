# -*- coding: utf-8 -*-

from zeep.settings import Settings
from zeep.wsdl import Document

from cvp.wsdl.transport import create_transport_with_package_asset


def create_document_with_package_asset(location: str):
    transport = create_transport_with_package_asset()
    return Document(
        location=location,
        transport=transport,  # noqa
        base=None,
        settings=Settings(),
    )

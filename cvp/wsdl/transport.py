# -*- coding: utf-8 -*-

from zeep.transports import Transport

from cvp.wsdl.cache import ZeepFileCache


def create_transport_with_package_asset():
    return Transport(cache=ZeepFileCache.with_package_asset())

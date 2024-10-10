# -*- coding: utf-8 -*-
# http://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl

from argparse import Namespace

from cvp.onvif.declarations import ONVIF_DECL_DEVICE_MANAGEMENT
from cvp.wsdl.service import create_service


def get_system_date_and_time(args: Namespace):
    service = create_service(ONVIF_DECL_DEVICE_MANAGEMENT, args)
    return service.GetSystemDateAndTime()


def get_capabilities(args: Namespace):
    """
    This method has been replaced by the more generic GetServices method.
    For capabilities of individual services refer to the GetServiceCapabilities methods.
    """
    service = create_service(ONVIF_DECL_DEVICE_MANAGEMENT, args)
    return service.GetCapabilities()


def get_services(args: Namespace):
    assert isinstance(args.IncludeCapability, bool)
    service = create_service(ONVIF_DECL_DEVICE_MANAGEMENT, args)
    return service.GetServices(IncludeCapability=args.IncludeCapability)


def get_device_information(args: Namespace):
    service = create_service(ONVIF_DECL_DEVICE_MANAGEMENT, args)
    return service.GetDeviceInformation()

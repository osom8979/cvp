# -*- coding: utf-8 -*-

from typing import Sequence

from cvp.wsdl.declaration import WsdlDeclaration

ONVIF_DECL_DEVICE_MANAGEMENT = WsdlDeclaration(
    declaration="http://www.onvif.org/ver10/device/wsdl",
    http_sub="device_service",
    wsdl_file="devicemgmt.wsdl",
    subclass="DeviceManagement",
    binding_names=["DeviceBinding"],
)

ONVIF_DECL_MEDIA = WsdlDeclaration(
    declaration="http://www.onvif.org/ver10/media/wsdl",
    http_sub="Media",
    wsdl_file="media.wsdl",
    subclass="Media",
    binding_names=["MediaBinding"],
)

ONVIF_DECL_EVENTS = WsdlDeclaration(
    declaration="http://www.onvif.org/ver10/events/wsdl",
    http_sub="Events",
    wsdl_file="events.wsdl",
    subclass="Events",
)

ONVIF_DECL_PTZ = WsdlDeclaration(
    declaration="http://www.onvif.org/ver20/ptz/wsdl",
    http_sub="PTZ",
    wsdl_file="ptz.wsdl",
    subclass="PTZ",
    binding_names=["PTZBinding"],
)

ONVIF_DECL_IMAGING = WsdlDeclaration(
    declaration="http://www.onvif.org/ver20/imaging/wsdl",
    http_sub="Imaging",
    wsdl_file="imaging.wsdl",
    subclass="Imaging",
    binding_names=["ImagingBinding"],
)

ONVIF_DECL_DEVICE_IO = WsdlDeclaration(
    declaration="http://www.onvif.org/ver10/deviceIO/wsdl",
    http_sub="DeviceIO",
    wsdl_file="deviceio.wsdl",
    subclass="DeviceIO",
)

ONVIF_DECL_ANALYTICS = WsdlDeclaration(
    declaration="http://www.onvif.org/ver20/analytics/wsdl",
    http_sub="Analytics",
    wsdl_file="analytics.wsdl",
    subclass="Analytics",
    binding_names=["RuleEngineBinding", "AnalyticsEngineBinding"],
)

ONVIF_DECLS: Sequence[WsdlDeclaration] = (
    ONVIF_DECL_DEVICE_MANAGEMENT,
    ONVIF_DECL_MEDIA,
    # ONVIF_DECL_EVENTS,
    ONVIF_DECL_PTZ,
    ONVIF_DECL_IMAGING,
    # ONVIF_DECL_DEVICE_IO,
    ONVIF_DECL_ANALYTICS,
)

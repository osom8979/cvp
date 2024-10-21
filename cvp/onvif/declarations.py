# -*- coding: utf-8 -*-

from typing import Final, Sequence

from cvp.wsdl.declaration import WsdlDeclaration

ONVIF_ANALYTICS: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver20/analytics/wsdl",
    location="http://www.onvif.org/ver20/analytics/wsdl/analytics.wsdl",
    binding="AnalyticsEngineBinding",
)

ONVIF_DEVICEIO: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/deviceIO/wsdl",
    location="http://www.onvif.org/ver10/deviceio.wsdl",
    binding="DeviceIOBinding",
)

ONVIF_DEVICEMGMT: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/device/wsdl",
    location="http://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl",
    binding="DeviceBinding",
)

ONVIF_EVENTS: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/events/wsdl",
    location="http://www.onvif.org/ver10/events/wsdl/event.wsdl",
    binding="EventBinding",
)

ONVIF_IMAGING: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver20/imaging/wsdl",
    location="http://www.onvif.org/ver20/imaging/wsdl/imaging.wsdl",
    binding="ImagingBinding",
)

ONVIF_MEDIA: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/media/wsdl",
    location="http://www.onvif.org/ver10/media/wsdl/media.wsdl",
    binding="MediaBinding",
)

ONVIF_NOTIFICATION: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/events/wsdl",
    location="http://www.onvif.org/ver10/events/wsdl/event.wsdl",
    binding="NotificationProducerBinding",
)

ONVIF_PTZ: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver20/ptz/wsdl",
    location="http://www.onvif.org/ver20/ptz/wsdl/ptz.wsdl",
    binding="PTZBinding",
)

ONVIF_PULLPOINT: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/events/wsdl",
    location="http://www.onvif.org/ver10/events/wsdl/event.wsdl",
    binding="PullPointSubscriptionBinding",
)

ONVIF_RECEIVER: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/receiver/wsdl",
    location="http://www.onvif.org/ver10/receiver.wsdl",
    binding="ReceiverBinding",
)

ONVIF_RECODING: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/recording/wsdl",
    location="http://www.onvif.org/ver10/recording.wsdl",
    binding="RecordingBinding",
)

ONVIF_REPLAY: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/replay/wsdl",
    location="http://www.onvif.org/ver10/replay.wsdl",
    binding="ReplayBinding",
)

ONVIF_SEARCH: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/search/wsdl",
    location="http://www.onvif.org/ver10/search.wsdl",
    binding="SearchBinding",
)

ONVIF_SUBSCRIPTION: Final[WsdlDeclaration] = WsdlDeclaration(
    namespace="http://www.onvif.org/ver10/events/wsdl",
    location="http://www.onvif.org/ver10/events/wsdl/event.wsdl",
    binding="SubscriptionManagerBinding",
)

ONVIF_DECLARATIONS: Sequence[WsdlDeclaration] = (
    ONVIF_ANALYTICS,
    ONVIF_DEVICEIO,
    ONVIF_DEVICEMGMT,
    ONVIF_EVENTS,
    ONVIF_IMAGING,
    ONVIF_MEDIA,
    ONVIF_NOTIFICATION,
    ONVIF_PTZ,
    ONVIF_PULLPOINT,
    ONVIF_RECEIVER,
    ONVIF_RECODING,
    ONVIF_REPLAY,
    ONVIF_SEARCH,
    ONVIF_SUBSCRIPTION,
)

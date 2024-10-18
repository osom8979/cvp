# -*- coding: utf-8 -*-

from typing import Dict, Optional, ParamSpec, Type, TypeVar

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.onvif.cache import has_response_use_cache_type, inject_response_cache
from cvp.onvif.service.analytics import OnvifAnalytics
from cvp.onvif.service.deviceio import OnvifDeviceIO
from cvp.onvif.service.devicemgmt import OnvifDeviceManagement
from cvp.onvif.service.events import OnvifEvents
from cvp.onvif.service.imaging import OnvifImaging
from cvp.onvif.service.media import OnvifMedia
from cvp.onvif.service.notification import OnvifNotification
from cvp.onvif.service.ptz import OnvifPTZ
from cvp.onvif.service.pullpoint import OnvifPullPoint
from cvp.onvif.service.receiver import OnvifReceiver
from cvp.onvif.service.recording import OnvifRecoding
from cvp.onvif.service.replay import OnvifReplay
from cvp.onvif.service.search import OnvifSearch
from cvp.onvif.service.subscription import OnvifSubscription
from cvp.onvif.types import Service
from cvp.resources.home import HomeDir
from cvp.wsdl.service import WsdlService

WsdlRequestParam = ParamSpec("WsdlRequestParam")
WsdlResponseT = TypeVar("WsdlResponseT")
WsdlServiceT = TypeVar("WsdlServiceT", bound=WsdlService)


def _create_wsdl_service(
    cls: Type[WsdlServiceT],
    onvif_config: OnvifConfig,
    wsdl_config: WsdlConfig,
    home: HomeDir,
    address: Optional[str] = None,
) -> WsdlServiceT:
    no_verify = onvif_config.no_verify
    no_cache = wsdl_config.no_cache
    cache_dir = str(home.wsdl)

    if onvif_config.use_wsse:
        with_http_basic = onvif_config.is_http_basic
        with_http_digest = onvif_config.is_http_digest
        username = onvif_config.username
        password = home.keyrings.get_onvif_password(onvif_config.uuid)
        use_digest = onvif_config.encode_digest
    else:
        with_http_basic = False
        with_http_digest = False
        username = None
        password = None
        use_digest = False

    service = cls(
        address=address if address else onvif_config.address,
        no_verify=no_verify,
        no_cache=no_cache,
        cache_dir=cache_dir,
        with_http_basic=with_http_basic,
        with_http_digest=with_http_digest,
        username=username,
        password=password,
        use_digest=use_digest,
        decl=None,
    )

    for key in dir(service):
        attr = getattr(service, key)
        if not has_response_use_cache_type(attr):
            continue

        injected_attr = inject_response_cache(
            attr,
            home,
            onvif_config,
            cls.__wsdl_declaration__,
        )
        setattr(service, key, injected_attr)

    return service


class OnvifService:
    _analytics: Optional[OnvifAnalytics]
    _deviceio: Optional[OnvifDeviceIO]
    _events: Optional[OnvifEvents]
    _imaging: Optional[OnvifImaging]
    _media: Optional[OnvifMedia]
    _notification: Optional[OnvifNotification]
    _ptz: Optional[OnvifPTZ]
    _pullpoint: Optional[OnvifPullPoint]
    _receiver: Optional[OnvifReceiver]
    _recording: Optional[OnvifRecoding]
    _replay: Optional[OnvifReplay]
    _search: Optional[OnvifSearch]
    _subscription: Optional[OnvifSubscription]
    _services: Dict[str, Service]

    def __init__(
        self,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
    ):
        self._devicemgmt = _create_wsdl_service(
            OnvifDeviceManagement,
            onvif_config,
            wsdl_config,
            home,
            onvif_config.address,
        )
        self._onvif_config = onvif_config
        self._wsdl_config = wsdl_config
        self._home = home

        self._analytics = None
        self._deviceio = None
        self._events = None
        self._imaging = None
        self._media = None
        self._notification = None
        self._ptz = None
        self._pullpoint = None
        self._receiver = None
        self._recording = None
        self._replay = None
        self._search = None
        self._subscription = None

        uuid = self._onvif_config.uuid
        binding = OnvifDeviceManagement.__wsdl_declaration__.binding
        api = OnvifDeviceManagement.get_services.__name__

        if self._home.onvifs.has_onvif_object(uuid, binding, api):
            services = self._home.onvifs.read_onvif_object(uuid, binding, api)
            self._services = {service.Namespace: service for service in services}
        else:
            self._services = dict()

    def clear(self):
        self._analytics = None
        self._deviceio = None
        self._events = None
        self._imaging = None
        self._media = None
        self._notification = None
        self._ptz = None
        self._pullpoint = None
        self._receiver = None
        self._recording = None
        self._replay = None
        self._search = None
        self._subscription = None
        self._services = dict()

    def update_services(self):
        response = self.devicemgmt.get_services(include_capability=False)
        self._services = {service.Namespace: service for service in response}
        return self._services

    def update_wsdl_services(self):
        wsdls = (
            self.devicemgmt,
            self.analytics,
            self.deviceio,
            self.events,
            self.imaging,
            self.media,
            self.notification,
            self.ptz,
            self.pullpoint,
            self.receiver,
            self.recording,
            self.replay,
            self.search,
            self.subscription,
        )
        return list(filter(lambda x: x is not None, wsdls))

    @property
    def devicemgmt(self):
        return self._devicemgmt

    def create_wsdl(self, cls: Type[WsdlServiceT]) -> Optional[WsdlServiceT]:
        namespace = cls.__wsdl_declaration__.namespace
        service = self._services.get(namespace)
        if service is None:
            return None

        return _create_wsdl_service(
            cls=cls,
            onvif_config=self._onvif_config,
            wsdl_config=self._wsdl_config,
            home=self._home,
            address=service.XAddr,
        )

    @property
    def analytics(self):
        if self._analytics is None:
            self._analytics = self.create_wsdl(OnvifAnalytics)
        return self._analytics

    @property
    def deviceio(self):
        if self._deviceio is None:
            self._deviceio = self.create_wsdl(OnvifDeviceIO)
        return self._deviceio

    @property
    def events(self):
        if self._events is None:
            self._events = self.create_wsdl(OnvifEvents)
        return self._events

    @property
    def imaging(self):
        if self._imaging is None:
            self._imaging = self.create_wsdl(OnvifImaging)
        return self._imaging

    @property
    def media(self):
        if self._media is None:
            self._media = self.create_wsdl(OnvifMedia)
        return self._media

    @property
    def notification(self):
        if self._notification is None:
            self._notification = self.create_wsdl(OnvifNotification)
        return self._notification

    @property
    def ptz(self):
        if self._ptz is None:
            self._ptz = self.create_wsdl(OnvifPTZ)
        return self._ptz

    @property
    def pullpoint(self):
        if self._pullpoint is None:
            self._pullpoint = self.create_wsdl(OnvifPullPoint)
        return self._pullpoint

    @property
    def receiver(self):
        if self._receiver is None:
            self._receiver = self.create_wsdl(OnvifReceiver)
        return self._receiver

    @property
    def recording(self):
        if self._recording is None:
            self._recording = self.create_wsdl(OnvifRecoding)
        return self._recording

    @property
    def replay(self):
        if self._replay is None:
            self._replay = self.create_wsdl(OnvifReplay)
        return self._replay

    @property
    def search(self):
        if self._search is None:
            self._search = self.create_wsdl(OnvifSearch)
        return self._search

    @property
    def subscription(self):
        if self._subscription is None:
            self._subscription = self.create_wsdl(OnvifSubscription)
        return self._subscription

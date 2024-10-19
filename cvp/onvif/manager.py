# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import List

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.onvif.service import OnvifService
from cvp.resources.home import HomeDir


class OnvifManager(OrderedDict[str, OnvifService]):
    def __init__(
        self,
        onvif_configs: List[OnvifConfig],
        wsdl_config: WsdlConfig,
        home: HomeDir,
        *,
        update=False
    ):
        super().__init__()
        self._onvif_configs = onvif_configs
        self._wsdl_config = wsdl_config
        self._home = home

        if onvif_configs and update:
            for onvif_config in onvif_configs:
                self.create_onvif_service(onvif_config, append=True)

    def create_onvif_service(self, onvif_config: OnvifConfig, *, append=False):
        service = OnvifService(
            onvif_config,
            self._wsdl_config,
            self._home,
        )
        if append:
            self.__setitem__(onvif_config.uuid, service)
        return service

    def sync(self, onvif_config: OnvifConfig) -> OnvifService:
        if self.__contains__(onvif_config.uuid):
            service = self.__getitem__(onvif_config.uuid)
            if service.onvif_config == onvif_config:
                return service
            else:
                self.__delitem__(onvif_config.uuid)
        return self.create_onvif_service(onvif_config, append=True)

# -*- coding: utf-8 -*-

from typing import Optional

from cvp.config.sections.onvif import OnvifConfig
from cvp.config.sections.wsdl import WsdlConfig
from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.service import OnvifService
from cvp.onvif.types import StreamType, TransportProtocol
from cvp.onvif.variables import ONVIF_V10_SCHEMA_URL, PROFILE_TOKEN_MAX_LENGTH
from cvp.resources.home import HomeDir
from cvp.wsdl.declaration import WsdlDeclaration

ONVIF_DECL_MEDIA = WsdlDeclaration(
    declaration="http://www.onvif.org/ver10/media/wsdl",
    http_sub="Media",
    wsdl_file="media.wsdl",
    subclass="Media",
    binding_names=["MediaBinding"],
)


class OnvifMedia(OnvifService):
    """
    http://www.onvif.org/ver10/media/wsdl/media.wsdl
    """

    def __init__(
        self,
        onvif_config: OnvifConfig,
        wsdl_config: WsdlConfig,
        home: HomeDir,
        password: Optional[str] = None,
    ):
        super().__init__(
            decl=ONVIF_DECL_MEDIA,
            onvif_config=onvif_config,
            wsdl_config=wsdl_config,
            home=home,
            password=password,
        )

    def get_profiles(self):
        return self.service.GetProfiles()

    def get_stream_uri(
        self,
        protocol: TransportProtocol,
        stream: StreamType,
        profile_token: str,
    ):
        if protocol == TransportProtocol.TCP:
            logger.warning(f"'{str(TransportProtocol.TCP)}' protocol is deprecated")

        if not (0 <= len(profile_token) <= PROFILE_TOKEN_MAX_LENGTH):
            raise ValueError(f"Invalid profile token length: '{profile_token}'")

        schema = self.client.type_factory(namespace=ONVIF_V10_SCHEMA_URL)
        transport = schema.Transport(Protocol=str(protocol))
        setup = schema.StreamSetup(Stream=str(stream), Transport=transport)
        return self.service.GetStreamUri(StreamSetup=setup, ProfileToken=profile_token)

    def get_snapshot_uri(self, profile_token: str):
        if not (0 <= len(profile_token) <= PROFILE_TOKEN_MAX_LENGTH):
            raise ValueError(f"Invalid profile token length: '{profile_token}'")

        return self.service.GetSnapshotUri(ProfileToken=profile_token)

# -*- coding: utf-8 -*-

from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.types import StreamType, TransportProtocol
from cvp.onvif.variables import ONVIF_V10_SCHEMA_URL, PROFILE_TOKEN_MAX_LENGTH
from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifMedia(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver10/media/wsdl",
        wsdl="http://www.onvif.org/ver10/media/wsdl/media.wsdl",
        binding="MediaBinding",
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

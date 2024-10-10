# -*- coding: utf-8 -*-
# http://www.onvif.org/ver10/media/wsdl/media.wsdl

from argparse import Namespace

from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.declarations import ONVIF_DECL_MEDIA
from cvp.onvif.variables import (
    ONVIF_V10_SCHEMA_URL,
    PROFILE_TOKEN_MAX_LENGTH,
    STREAM_TYPES,
    TRANSPORT_PROTOCOL_TCP,
    TRANSPORT_PROTOCOLS,
)
from cvp.wsdl.service import create_client_and_service, create_service


def get_profiles(args: Namespace):
    service = create_service(ONVIF_DECL_MEDIA, args)
    return service.GetProfiles()


def get_stream_uri(args: Namespace):
    assert isinstance(args.Protocol, str)
    assert isinstance(args.Stream, str)
    assert isinstance(args.ProfileToken, str)
    assert args.Protocol in TRANSPORT_PROTOCOLS
    if args.Protocol == TRANSPORT_PROTOCOL_TCP:
        logger.warning(f"'{TRANSPORT_PROTOCOL_TCP}' protocol is deprecated")
    assert args.Stream in STREAM_TYPES
    assert len(args.ProfileToken) <= PROFILE_TOKEN_MAX_LENGTH

    client, service = create_client_and_service(ONVIF_DECL_MEDIA, args)
    schema = client.type_factory(namespace=ONVIF_V10_SCHEMA_URL)
    transport = schema.Transport(Protocol=args.Protocol)
    setup = schema.StreamSetup(Stream=args.Stream, Transport=transport)
    return service.GetStreamUri(StreamSetup=setup, ProfileToken=args.ProfileToken)


def get_snapshot_uri(args: Namespace):
    assert isinstance(args.ProfileToken, str)
    assert len(args.ProfileToken) <= PROFILE_TOKEN_MAX_LENGTH

    service = create_service(ONVIF_DECL_MEDIA, args)
    return service.GetSnapshotUri(ProfileToken=args.ProfileToken)

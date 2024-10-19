# -*- coding: utf-8 -*-

from functools import wraps
from typing import Final

from cvp.config.sections.onvif import OnvifConfig
from cvp.resources.home import HomeDir
from cvp.wsdl.declaration import WsdlDeclaration

ONVIF_API_ATTR_NAME: Final[str] = "__onvif_api__"


def has_onvif_api(func) -> bool:
    return hasattr(func, ONVIF_API_ATTR_NAME)


def get_onvif_api(func) -> bool:
    return getattr(func, ONVIF_API_ATTR_NAME, False)


def set_onvif_api(func) -> None:
    setattr(func, ONVIF_API_ATTR_NAME, True)


def onvif_api(func):
    set_onvif_api(func)

    @wraps(func)
    def _func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return _func_wrapper


def inject_response_cache(
    func,
    home: HomeDir,
    onvif_config: OnvifConfig,
    wsdl: WsdlDeclaration,
):
    @wraps(func)
    def _func_wrapper(*args, **kwargs):
        uuid = onvif_config.uuid
        binding = wsdl.binding
        api = func.__name__

        if home.onvifs.has_onvif_object(uuid, binding, api):
            return home.onvifs.read_onvif_object(uuid, binding, api)
        else:
            response = func(*args, **kwargs)
            home.onvifs.write_onvif_object(uuid, binding, api, response)
            return response

    return _func_wrapper

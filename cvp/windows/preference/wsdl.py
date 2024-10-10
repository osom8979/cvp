# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.logging.logging import logger
from cvp.types import override
from cvp.windows.preference._base import PreferenceWidget


class WsdlPreference(PreferenceWidget):
    def __init__(self, context: Context, label="WSDL"):
        self._config = context.config.wsdl
        self._label = label

    @property
    @override
    def label(self) -> str:
        return self._label

    @override
    def on_process(self) -> None:
        no_verify_result = imgui.checkbox("No SSL Verify", self._config.no_verify)
        no_verify_changed = no_verify_result[0]
        no_verify_value = no_verify_result[1]
        assert isinstance(no_verify_changed, bool)
        assert isinstance(no_verify_value, bool)
        if no_verify_changed:
            self._config.no_verify = no_verify_value
            if no_verify_value:
                logger.info("Disabling SSL certificate verification")
            else:
                logger.info("Enabling SSL certificate verification")

        no_cache_result = imgui.checkbox("No Cache File", self._config.no_cache)
        no_cache_changed = no_cache_result[0]
        no_cache_value = no_cache_result[1]
        assert isinstance(no_cache_changed, bool)
        assert isinstance(no_cache_value, bool)
        if no_cache_changed:
            self._config.no_cache = no_cache_value
            if no_cache_value:
                logger.info("Do not save the WSDL schema as a file")
            else:
                logger.info("Save the WSDL schema as a file")

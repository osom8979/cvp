# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifAnalytics(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver20/analytics/wsdl",
        wsdl="http://www.onvif.org/ver20/analytics/wsdl/analytics.wsdl",
        binding="AnalyticsEngineBinding",
    )

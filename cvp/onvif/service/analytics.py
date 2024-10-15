# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifAnalytics(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        declaration="http://www.onvif.org/ver20/analytics/wsdl",
        http_sub="Analytics",
        wsdl_file="analytics.wsdl",
        subclass="Analytics",
        binding_names=["RuleEngineBinding", "AnalyticsEngineBinding"],
    )

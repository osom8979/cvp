# -*- coding: utf-8 -*-

from cvp.wsdl.declaration import WsdlDeclaration
from cvp.wsdl.service import WsdlService


class OnvifSubscription(WsdlService):
    __wsdl_declaration__ = WsdlDeclaration(
        namespace="http://www.onvif.org/ver10/events/wsdl",
        wsdl="http://www.onvif.org/ver10/events/wsdl/event.wsdl",
        binding="SubscriptionManagerBinding",
    )

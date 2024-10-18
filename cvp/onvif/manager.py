# -*- coding: utf-8 -*-

from collections import OrderedDict

from cvp.onvif.service import OnvifService


class OnvifManager(OrderedDict[str, OnvifService]):
    pass

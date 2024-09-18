# -*- coding: utf-8 -*-

from abc import ABC

from cvp.pgc.constants.blend_flag import BlendFlag as _BlendFlag
from cvp.pgc.constants.button_type import ButtonType as _ButtonType
from cvp.pgc.constants.display_flag import DisplayFlag as _DisplayFlag
from cvp.pgc.constants.event_type import EventType as _EventType
from cvp.pgc.constants.keycode import Keycode as _Keycode
from cvp.pgc.constants.keymod import Keymod as _Keymod
from cvp.pgc.constants.surface_flag import SurfaceFlag as _SurfaceFlag


class Constants(ABC):
    BlendFlag = _BlendFlag
    ButtonType = _ButtonType
    DisplayFlag = _DisplayFlag
    EventType = _EventType
    Keycode = _Keycode
    Keymod = _Keymod
    SurfaceFlag = _SurfaceFlag

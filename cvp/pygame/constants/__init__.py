# -*- coding: utf-8 -*-

from abc import ABC

from cvp.pygame.constants.blend_flag import BlendFlag as _BlendFlag
from cvp.pygame.constants.button_type import ButtonType as _ButtonType
from cvp.pygame.constants.display_flag import DisplayFlag as _DisplayFlag
from cvp.pygame.constants.event_type import EventType as _EventType
from cvp.pygame.constants.keycode import Keycode as _Keycode
from cvp.pygame.constants.keymod import Keymod as _Keymod
from cvp.pygame.constants.surface_flag import SurfaceFlag as _SurfaceFlag


class Constants(ABC):
    BlendFlag = _BlendFlag
    ButtonType = _ButtonType
    DisplayFlag = _DisplayFlag
    EventType = _EventType
    Keycode = _Keycode
    Keymod = _Keymod
    SurfaceFlag = _SurfaceFlag

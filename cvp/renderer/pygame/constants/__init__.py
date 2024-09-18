# -*- coding: utf-8 -*-

from abc import ABC

from cvp.renderer.pygame.constants.blend_flag import BlendFlag as _BlendFlag
from cvp.renderer.pygame.constants.button_type import ButtonType as _ButtonType
from cvp.renderer.pygame.constants.display_flag import DisplayFlag as _DisplayFlag
from cvp.renderer.pygame.constants.event_type import EventType as _EventType
from cvp.renderer.pygame.constants.keycode import Keycode as _Keycode
from cvp.renderer.pygame.constants.keymod import Keymod as _Keymod
from cvp.renderer.pygame.constants.surface_flag import SurfaceFlag as _SurfaceFlag


class Constants(ABC):
    BlendFlag = _BlendFlag
    ButtonType = _ButtonType
    DisplayFlag = _DisplayFlag
    EventType = _EventType
    Keycode = _Keycode
    Keymod = _Keymod
    SurfaceFlag = _SurfaceFlag

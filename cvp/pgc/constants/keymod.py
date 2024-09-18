# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from typing import Dict, Final, NamedTuple

from pygame import constants


@unique
class Keymod(IntFlag):
    NONE = constants.KMOD_NONE
    LSHIFT = constants.KMOD_LSHIFT
    RSHIFT = constants.KMOD_RSHIFT
    SHIFT = constants.KMOD_SHIFT
    LCTRL = constants.KMOD_LCTRL
    RCTRL = constants.KMOD_RCTRL
    CTRL = constants.KMOD_CTRL
    LALT = constants.KMOD_LALT
    RALT = constants.KMOD_RALT
    ALT = constants.KMOD_ALT
    LMETA = constants.KMOD_LMETA
    RMETA = constants.KMOD_RMETA
    META = constants.KMOD_META
    CAPS = constants.KMOD_CAPS
    NUM = constants.KMOD_NUM
    MODE = constants.KMOD_MODE


class KeymodInfo(NamedTuple):
    constant: int
    description: str


# fmt: off
KEYMOD_INFO_MAP: Final[Dict[Keymod, KeymodInfo]] = {
    Keymod.NONE: KeymodInfo(constants.KMOD_NONE, "no modifier keys pressed"),
    Keymod.LSHIFT: KeymodInfo(constants.KMOD_LSHIFT, "left shift"),
    Keymod.RSHIFT: KeymodInfo(constants.KMOD_RSHIFT, "right shift"),
    Keymod.SHIFT: KeymodInfo(constants.KMOD_SHIFT, "left shift or right shift or both"),
    Keymod.LCTRL: KeymodInfo(constants.KMOD_LCTRL, "left control"),
    Keymod.RCTRL: KeymodInfo(constants.KMOD_RCTRL, "right control"),
    Keymod.CTRL: KeymodInfo(constants.KMOD_CTRL, "left control or right control or both"),  # noqa: E501
    Keymod.LALT: KeymodInfo(constants.KMOD_LALT, "left alt"),
    Keymod.RALT: KeymodInfo(constants.KMOD_RALT, "right alt"),
    Keymod.ALT: KeymodInfo(constants.KMOD_ALT, "left alt or right alt or both"),
    Keymod.LMETA: KeymodInfo(constants.KMOD_LMETA, "left meta"),
    Keymod.RMETA: KeymodInfo(constants.KMOD_RMETA, "right meta"),
    Keymod.META: KeymodInfo(constants.KMOD_META, "left meta or right meta or both"),
    Keymod.CAPS: KeymodInfo(constants.KMOD_CAPS, "caps lock"),
    Keymod.NUM: KeymodInfo(constants.KMOD_NUM, "num lock"),
    Keymod.MODE: KeymodInfo(constants.KMOD_MODE, "AltGr"),
}
# fmt: on

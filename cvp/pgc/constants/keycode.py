# -*- coding: utf-8 -*-

from enum import IntEnum
from typing import Dict, Final, NamedTuple, Optional

from pygame import constants


class Keycode(IntEnum):
    BACKSPACE = constants.K_BACKSPACE
    TAB = constants.K_TAB
    CLEAR = constants.K_CLEAR
    RETURN = constants.K_RETURN
    PAUSE = constants.K_PAUSE
    ESCAPE = constants.K_ESCAPE
    SPACE = constants.K_SPACE
    EXCLAIM = constants.K_EXCLAIM
    QUOTEDBL = constants.K_QUOTEDBL
    HASH = constants.K_HASH
    DOLLAR = constants.K_DOLLAR
    AMPERSAND = constants.K_AMPERSAND
    QUOTE = constants.K_QUOTE
    LEFTPAREN = constants.K_LEFTPAREN
    RIGHTPAREN = constants.K_RIGHTPAREN
    ASTERISK = constants.K_ASTERISK
    PLUS = constants.K_PLUS
    COMMA = constants.K_COMMA
    MINUS = constants.K_MINUS
    PERIOD = constants.K_PERIOD
    SLASH = constants.K_SLASH
    NUM_0 = constants.K_0
    NUM_1 = constants.K_1
    NUM_2 = constants.K_2
    NUM_3 = constants.K_3
    NUM_4 = constants.K_4
    NUM_5 = constants.K_5
    NUM_6 = constants.K_6
    NUM_7 = constants.K_7
    NUM_8 = constants.K_8
    NUM_9 = constants.K_9
    COLON = constants.K_COLON
    SEMICOLON = constants.K_SEMICOLON
    LESS = constants.K_LESS
    EQUALS = constants.K_EQUALS
    GREATER = constants.K_GREATER
    QUESTION = constants.K_QUESTION
    AT = constants.K_AT
    LEFTBRACKET = constants.K_LEFTBRACKET
    BACKSLASH = constants.K_BACKSLASH
    RIGHTBRACKET = constants.K_RIGHTBRACKET
    CARET = constants.K_CARET
    UNDERSCORE = constants.K_UNDERSCORE
    BACKQUOTE = constants.K_BACKQUOTE
    ALPHA_A = constants.K_a
    ALPHA_B = constants.K_b
    ALPHA_C = constants.K_c
    ALPHA_D = constants.K_d
    ALPHA_E = constants.K_e
    ALPHA_F = constants.K_f
    ALPHA_G = constants.K_g
    ALPHA_H = constants.K_h
    ALPHA_I = constants.K_i
    ALPHA_J = constants.K_j
    ALPHA_K = constants.K_k
    ALPHA_L = constants.K_l
    ALPHA_M = constants.K_m
    ALPHA_N = constants.K_n
    ALPHA_O = constants.K_o
    ALPHA_P = constants.K_p
    ALPHA_Q = constants.K_q
    ALPHA_R = constants.K_r
    ALPHA_S = constants.K_s
    ALPHA_T = constants.K_t
    ALPHA_U = constants.K_u
    ALPHA_V = constants.K_v
    ALPHA_W = constants.K_w
    ALPHA_X = constants.K_x
    ALPHA_Y = constants.K_y
    ALPHA_Z = constants.K_z
    DELETE = constants.K_DELETE
    KP0 = constants.K_KP0
    KP1 = constants.K_KP1
    KP2 = constants.K_KP2
    KP3 = constants.K_KP3
    KP4 = constants.K_KP4
    KP5 = constants.K_KP5
    KP6 = constants.K_KP6
    KP7 = constants.K_KP7
    KP8 = constants.K_KP8
    KP9 = constants.K_KP9
    KP_PERIOD = constants.K_KP_PERIOD
    KP_DIVIDE = constants.K_KP_DIVIDE
    KP_MULTIPLY = constants.K_KP_MULTIPLY
    KP_MINUS = constants.K_KP_MINUS
    KP_PLUS = constants.K_KP_PLUS
    KP_ENTER = constants.K_KP_ENTER
    KP_EQUALS = constants.K_KP_EQUALS
    UP = constants.K_UP
    DOWN = constants.K_DOWN
    RIGHT = constants.K_RIGHT
    LEFT = constants.K_LEFT
    INSERT = constants.K_INSERT
    HOME = constants.K_HOME
    END = constants.K_END
    PAGEUP = constants.K_PAGEUP
    PAGEDOWN = constants.K_PAGEDOWN
    F1 = constants.K_F1
    F2 = constants.K_F2
    F3 = constants.K_F3
    F4 = constants.K_F4
    F5 = constants.K_F5
    F6 = constants.K_F6
    F7 = constants.K_F7
    F8 = constants.K_F8
    F9 = constants.K_F9
    F10 = constants.K_F10
    F11 = constants.K_F11
    F12 = constants.K_F12
    F13 = constants.K_F13
    F14 = constants.K_F14
    F15 = constants.K_F15
    NUMLOCK = constants.K_NUMLOCK
    CAPSLOCK = constants.K_CAPSLOCK
    SCROLLOCK = constants.K_SCROLLOCK
    RSHIFT = constants.K_RSHIFT
    LSHIFT = constants.K_LSHIFT
    RCTRL = constants.K_RCTRL
    LCTRL = constants.K_LCTRL
    RALT = constants.K_RALT
    LALT = constants.K_LALT
    RMETA = constants.K_RMETA
    LMETA = constants.K_LMETA
    LSUPER = constants.K_LSUPER
    RSUPER = constants.K_RSUPER
    MODE = constants.K_MODE
    HELP = constants.K_HELP
    PRINT = constants.K_PRINT
    SYSREQ = constants.K_SYSREQ
    BREAK = constants.K_BREAK
    MENU = constants.K_MENU
    POWER = constants.K_POWER
    EURO = constants.K_EURO
    AC_BACK = constants.K_AC_BACK


class KeycodeInfo(NamedTuple):
    constant: int
    character: Optional[str]
    description: str


KEYCODE_INFO_MAP: Final[Dict[Keycode, KeycodeInfo]] = {
    Keycode.BACKSPACE: KeycodeInfo(constants.K_BACKSPACE, "\b", "backspace"),
    Keycode.TAB: KeycodeInfo(constants.K_TAB, "\t", "tab"),
    Keycode.CLEAR: KeycodeInfo(constants.K_CLEAR, None, "clear"),
    Keycode.RETURN: KeycodeInfo(constants.K_RETURN, "\r", "return"),
    Keycode.PAUSE: KeycodeInfo(constants.K_PAUSE, None, "pause"),
    Keycode.ESCAPE: KeycodeInfo(constants.K_ESCAPE, "^[", "escape"),
    Keycode.SPACE: KeycodeInfo(constants.K_SPACE, None, "space"),
    Keycode.EXCLAIM: KeycodeInfo(constants.K_EXCLAIM, "!", "exclaim"),
    Keycode.QUOTEDBL: KeycodeInfo(constants.K_QUOTEDBL, '"', "quotedbl"),
    Keycode.HASH: KeycodeInfo(constants.K_HASH, "#", "hash"),
    Keycode.DOLLAR: KeycodeInfo(constants.K_DOLLAR, "$", "dollar"),
    Keycode.AMPERSAND: KeycodeInfo(constants.K_AMPERSAND, "&", "ampersand"),
    Keycode.QUOTE: KeycodeInfo(constants.K_QUOTE, None, "quote"),
    Keycode.LEFTPAREN: KeycodeInfo(constants.K_LEFTPAREN, "(", "left parenthesis"),
    Keycode.RIGHTPAREN: KeycodeInfo(constants.K_RIGHTPAREN, ")", "right parenthesis"),
    Keycode.ASTERISK: KeycodeInfo(constants.K_ASTERISK, "*", "asterisk"),
    Keycode.PLUS: KeycodeInfo(constants.K_PLUS, "+", "plus sign"),
    Keycode.COMMA: KeycodeInfo(constants.K_COMMA, ",", "comma"),
    Keycode.MINUS: KeycodeInfo(constants.K_MINUS, "-", "minus sign"),
    Keycode.PERIOD: KeycodeInfo(constants.K_PERIOD, ".", "period"),
    Keycode.SLASH: KeycodeInfo(constants.K_SLASH, "/", "forward slash"),
    Keycode.NUM_0: KeycodeInfo(constants.K_0, "0", "0"),
    Keycode.NUM_1: KeycodeInfo(constants.K_1, "1", "1"),
    Keycode.NUM_2: KeycodeInfo(constants.K_2, "2", "2"),
    Keycode.NUM_3: KeycodeInfo(constants.K_3, "3", "3"),
    Keycode.NUM_4: KeycodeInfo(constants.K_4, "4", "4"),
    Keycode.NUM_5: KeycodeInfo(constants.K_5, "5", "5"),
    Keycode.NUM_6: KeycodeInfo(constants.K_6, "6", "6"),
    Keycode.NUM_7: KeycodeInfo(constants.K_7, "7", "7"),
    Keycode.NUM_8: KeycodeInfo(constants.K_8, "8", "8"),
    Keycode.NUM_9: KeycodeInfo(constants.K_9, "9", "9"),
    Keycode.COLON: KeycodeInfo(constants.K_COLON, ":", "colon"),
    Keycode.SEMICOLON: KeycodeInfo(constants.K_SEMICOLON, ";", "semicolon"),
    Keycode.LESS: KeycodeInfo(constants.K_LESS, "<", "less-than sign"),
    Keycode.EQUALS: KeycodeInfo(constants.K_EQUALS, "=", "equals sign"),
    Keycode.GREATER: KeycodeInfo(constants.K_GREATER, ">", "greater-than sign"),
    Keycode.QUESTION: KeycodeInfo(constants.K_QUESTION, "?", "question mark"),
    Keycode.AT: KeycodeInfo(constants.K_AT, "@", "at"),
    Keycode.LEFTBRACKET: KeycodeInfo(constants.K_LEFTBRACKET, "[", "left bracket"),
    Keycode.BACKSLASH: KeycodeInfo(constants.K_BACKSLASH, "\\", "backslash"),
    Keycode.RIGHTBRACKET: KeycodeInfo(constants.K_RIGHTBRACKET, "]", "right bracket"),
    Keycode.CARET: KeycodeInfo(constants.K_CARET, "^", "caret"),
    Keycode.UNDERSCORE: KeycodeInfo(constants.K_UNDERSCORE, "_", "underscore"),
    Keycode.BACKQUOTE: KeycodeInfo(constants.K_BACKQUOTE, "`", "grave"),
    Keycode.ALPHA_A: KeycodeInfo(constants.K_a, "a", "alphabet a"),
    Keycode.ALPHA_B: KeycodeInfo(constants.K_b, "b", "alphabet b"),
    Keycode.ALPHA_C: KeycodeInfo(constants.K_c, "c", "alphabet c"),
    Keycode.ALPHA_D: KeycodeInfo(constants.K_d, "d", "alphabet d"),
    Keycode.ALPHA_E: KeycodeInfo(constants.K_e, "e", "alphabet e"),
    Keycode.ALPHA_F: KeycodeInfo(constants.K_f, "f", "alphabet f"),
    Keycode.ALPHA_G: KeycodeInfo(constants.K_g, "g", "alphabet g"),
    Keycode.ALPHA_H: KeycodeInfo(constants.K_h, "h", "alphabet h"),
    Keycode.ALPHA_I: KeycodeInfo(constants.K_i, "i", "alphabet i"),
    Keycode.ALPHA_J: KeycodeInfo(constants.K_j, "j", "alphabet j"),
    Keycode.ALPHA_K: KeycodeInfo(constants.K_k, "k", "alphabet k"),
    Keycode.ALPHA_L: KeycodeInfo(constants.K_l, "l", "alphabet l"),
    Keycode.ALPHA_M: KeycodeInfo(constants.K_m, "m", "alphabet m"),
    Keycode.ALPHA_N: KeycodeInfo(constants.K_n, "n", "alphabet n"),
    Keycode.ALPHA_O: KeycodeInfo(constants.K_o, "o", "alphabet o"),
    Keycode.ALPHA_P: KeycodeInfo(constants.K_p, "p", "alphabet p"),
    Keycode.ALPHA_Q: KeycodeInfo(constants.K_q, "q", "alphabet q"),
    Keycode.ALPHA_R: KeycodeInfo(constants.K_r, "r", "alphabet r"),
    Keycode.ALPHA_S: KeycodeInfo(constants.K_s, "s", "alphabet s"),
    Keycode.ALPHA_T: KeycodeInfo(constants.K_t, "t", "alphabet t"),
    Keycode.ALPHA_U: KeycodeInfo(constants.K_u, "u", "alphabet u"),
    Keycode.ALPHA_V: KeycodeInfo(constants.K_v, "v", "alphabet v"),
    Keycode.ALPHA_W: KeycodeInfo(constants.K_w, "w", "alphabet w"),
    Keycode.ALPHA_X: KeycodeInfo(constants.K_x, "x", "alphabet x"),
    Keycode.ALPHA_Y: KeycodeInfo(constants.K_y, "y", "alphabet y"),
    Keycode.ALPHA_Z: KeycodeInfo(constants.K_z, "z", "alphabet z"),
    Keycode.DELETE: KeycodeInfo(constants.K_DELETE, None, "delete"),
    Keycode.KP0: KeycodeInfo(constants.K_KP0, None, "keypad 0"),
    Keycode.KP1: KeycodeInfo(constants.K_KP1, None, "keypad 1"),
    Keycode.KP2: KeycodeInfo(constants.K_KP2, None, "keypad 2"),
    Keycode.KP3: KeycodeInfo(constants.K_KP3, None, "keypad 3"),
    Keycode.KP4: KeycodeInfo(constants.K_KP4, None, "keypad 4"),
    Keycode.KP5: KeycodeInfo(constants.K_KP5, None, "keypad 5"),
    Keycode.KP6: KeycodeInfo(constants.K_KP6, None, "keypad 6"),
    Keycode.KP7: KeycodeInfo(constants.K_KP7, None, "keypad 7"),
    Keycode.KP8: KeycodeInfo(constants.K_KP8, None, "keypad 8"),
    Keycode.KP9: KeycodeInfo(constants.K_KP9, None, "keypad 9"),
    Keycode.KP_PERIOD: KeycodeInfo(constants.K_KP_PERIOD, ".", "keypad period"),
    Keycode.KP_DIVIDE: KeycodeInfo(constants.K_KP_DIVIDE, "/", "keypad divide"),
    Keycode.KP_MULTIPLY: KeycodeInfo(constants.K_KP_MULTIPLY, "*", "keypad multiply"),
    Keycode.KP_MINUS: KeycodeInfo(constants.K_KP_MINUS, "-", "keypad minus"),
    Keycode.KP_PLUS: KeycodeInfo(constants.K_KP_PLUS, "+", "keypad plus"),
    Keycode.KP_ENTER: KeycodeInfo(constants.K_KP_ENTER, "\r", "keypad enter"),
    Keycode.KP_EQUALS: KeycodeInfo(constants.K_KP_EQUALS, "=", "keypad equals"),
    Keycode.UP: KeycodeInfo(constants.K_UP, None, "up arrow"),
    Keycode.DOWN: KeycodeInfo(constants.K_DOWN, None, "down arrow"),
    Keycode.RIGHT: KeycodeInfo(constants.K_RIGHT, None, "right arrow"),
    Keycode.LEFT: KeycodeInfo(constants.K_LEFT, None, "left arrow"),
    Keycode.INSERT: KeycodeInfo(constants.K_INSERT, None, "insert"),
    Keycode.HOME: KeycodeInfo(constants.K_HOME, None, "home"),
    Keycode.END: KeycodeInfo(constants.K_END, None, "end"),
    Keycode.PAGEUP: KeycodeInfo(constants.K_PAGEUP, None, "page up"),
    Keycode.PAGEDOWN: KeycodeInfo(constants.K_PAGEDOWN, None, "page down"),
    Keycode.F1: KeycodeInfo(constants.K_F1, None, "F1"),
    Keycode.F2: KeycodeInfo(constants.K_F2, None, "F2"),
    Keycode.F3: KeycodeInfo(constants.K_F3, None, "F3"),
    Keycode.F4: KeycodeInfo(constants.K_F4, None, "F4"),
    Keycode.F5: KeycodeInfo(constants.K_F5, None, "F5"),
    Keycode.F6: KeycodeInfo(constants.K_F6, None, "F6"),
    Keycode.F7: KeycodeInfo(constants.K_F7, None, "F7"),
    Keycode.F8: KeycodeInfo(constants.K_F8, None, "F8"),
    Keycode.F9: KeycodeInfo(constants.K_F9, None, "F9"),
    Keycode.F10: KeycodeInfo(constants.K_F10, None, "F10"),
    Keycode.F11: KeycodeInfo(constants.K_F11, None, "F11"),
    Keycode.F12: KeycodeInfo(constants.K_F12, None, "F12"),
    Keycode.F13: KeycodeInfo(constants.K_F13, None, "F13"),
    Keycode.F14: KeycodeInfo(constants.K_F14, None, "F14"),
    Keycode.F15: KeycodeInfo(constants.K_F15, None, "F15"),
    Keycode.NUMLOCK: KeycodeInfo(constants.K_NUMLOCK, None, "num lock"),
    Keycode.CAPSLOCK: KeycodeInfo(constants.K_CAPSLOCK, None, "caps lock"),
    Keycode.SCROLLOCK: KeycodeInfo(constants.K_SCROLLOCK, None, "scroll lock"),
    Keycode.RSHIFT: KeycodeInfo(constants.K_RSHIFT, None, "right shift"),
    Keycode.LSHIFT: KeycodeInfo(constants.K_LSHIFT, None, "left shift"),
    Keycode.RCTRL: KeycodeInfo(constants.K_RCTRL, None, "right control"),
    Keycode.LCTRL: KeycodeInfo(constants.K_LCTRL, None, "left control"),
    Keycode.RALT: KeycodeInfo(constants.K_RALT, None, "right alt"),
    Keycode.LALT: KeycodeInfo(constants.K_LALT, None, "left alt"),
    Keycode.RMETA: KeycodeInfo(constants.K_RMETA, None, "right meta"),
    Keycode.LMETA: KeycodeInfo(constants.K_LMETA, None, "left meta"),
    Keycode.LSUPER: KeycodeInfo(constants.K_LSUPER, None, "left Windows key"),
    Keycode.RSUPER: KeycodeInfo(constants.K_RSUPER, None, "right Windows key"),
    Keycode.MODE: KeycodeInfo(constants.K_MODE, None, "mode shift"),
    Keycode.HELP: KeycodeInfo(constants.K_HELP, None, "help"),
    Keycode.PRINT: KeycodeInfo(constants.K_PRINT, None, "print screen"),
    Keycode.SYSREQ: KeycodeInfo(constants.K_SYSREQ, None, "system request"),
    Keycode.BREAK: KeycodeInfo(constants.K_BREAK, None, "break"),
    Keycode.MENU: KeycodeInfo(constants.K_MENU, None, "menu"),
    Keycode.POWER: KeycodeInfo(constants.K_POWER, None, "power"),
    Keycode.EURO: KeycodeInfo(constants.K_EURO, None, "Euro"),
    Keycode.AC_BACK: KeycodeInfo(constants.K_AC_BACK, None, "android back button"),
}

# -*- coding: utf-8 -*-

from abc import ABC

from cvp.transitions import easing as _easing
from cvp.transitions.easing import EasingCallable


class EasingFunctions(ABC):
    linear: EasingCallable = _easing.linear
    ease_in_sine: EasingCallable = _easing.ease_in_sine
    ease_out_sine: EasingCallable = _easing.ease_out_sine
    ease_in_out_sine: EasingCallable = _easing.ease_in_out_sine
    ease_in_quad: EasingCallable = _easing.ease_in_quad
    ease_out_quad: EasingCallable = _easing.ease_out_quad
    ease_in_out_quad: EasingCallable = _easing.ease_in_out_quad
    ease_in_cubic: EasingCallable = _easing.ease_in_cubic
    ease_out_cubic: EasingCallable = _easing.ease_out_cubic
    ease_in_out_cubic: EasingCallable = _easing.ease_in_out_cubic
    ease_in_quart: EasingCallable = _easing.ease_in_quart
    ease_out_quart: EasingCallable = _easing.ease_out_quart
    ease_in_out_quart: EasingCallable = _easing.ease_in_out_quart
    ease_in_quint: EasingCallable = _easing.ease_in_quint
    ease_out_quint: EasingCallable = _easing.ease_out_quint
    ease_in_out_quint: EasingCallable = _easing.ease_in_out_quint
    ease_in_expo: EasingCallable = _easing.ease_in_expo
    ease_out_expo: EasingCallable = _easing.ease_out_expo
    ease_in_out_expo: EasingCallable = _easing.ease_in_out_expo
    ease_in_circ: EasingCallable = _easing.ease_in_circ
    ease_out_circ: EasingCallable = _easing.ease_out_circ
    ease_in_out_circ: EasingCallable = _easing.ease_in_out_circ
    ease_in_back: EasingCallable = _easing.ease_in_back
    ease_out_back: EasingCallable = _easing.ease_out_back
    ease_in_out_back: EasingCallable = _easing.ease_in_out_back
    ease_in_elastic: EasingCallable = _easing.ease_in_elastic
    ease_out_elastic: EasingCallable = _easing.ease_out_elastic
    ease_in_out_elastic: EasingCallable = _easing.ease_in_out_elastic
    ease_in_bounce: EasingCallable = _easing.ease_in_bounce
    ease_out_bounce: EasingCallable = _easing.ease_out_bounce
    ease_in_out_bounce: EasingCallable = _easing.ease_in_out_bounce

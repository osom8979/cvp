# -*- coding: utf-8 -*-


def measure_fade_ratio(
    elapsed: float,
    fadein: float,
    waiting: float,
    fadeout: float,
) -> float:
    if elapsed <= fadein:
        return elapsed / fadein
    elif elapsed <= fadein + waiting:
        return 1.0
    elif elapsed <= fadein + waiting + fadeout:
        return 1.0 - (elapsed - fadein - waiting) / fadeout
    else:
        raise ValueError("Exceeded fade range")

# -*- coding: utf-8 -*-

from dataclasses import fields, is_dataclass


def public_eq(cls):
    assert is_dataclass(cls)

    def __eq__(lh, rh):
        if not isinstance(lh, cls):
            return False
        if not isinstance(rh, cls):
            return False

        for f in fields(lh):
            if f.name.startswith("_"):
                continue
            if getattr(lh, f.name) != getattr(rh, f.name):
                return False
        return True

    cls.__eq__ = __eq__
    return cls

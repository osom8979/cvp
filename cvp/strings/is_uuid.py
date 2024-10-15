# -*- coding: utf-8 -*-

from uuid import UUID


def is_uuid(text: str, expect_version: int) -> bool:
    try:
        uuid_obj = UUID(text)
        return uuid_obj.version == expect_version
    except ValueError:
        return False


def is_uuid4(text: str) -> bool:
    return is_uuid(text, 4)

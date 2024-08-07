# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final, List, Sequence

from cvp.config._base import BaseConfig
from cvp.config.sections._base import BaseSection

_SECTION_PREFIX: Final[str] = "av."
_SECTION_PREFIX_LEN: Final[int] = len(_SECTION_PREFIX)


def join_av_section_name(name: str) -> str:
    return f"{_SECTION_PREFIX}{name}"


def split_av_name(section: str) -> str:
    if not section.startswith(_SECTION_PREFIX):
        raise ValueError(f"'{section}' does not start with '{_SECTION_PREFIX}'")

    return section[_SECTION_PREFIX_LEN:]


def _av_section_filter(key: str) -> bool:
    return key.startswith(AvSection.PREFIX)


def filter_av_sections(sections: Sequence[str]) -> List[str]:
    return list(filter(_av_section_filter, sections))


@unique
class _Keys(StrEnum):
    opened = auto()


class AvSection(BaseSection):
    PREFIX = _SECTION_PREFIX
    K = _Keys

    def __init__(self, section: str, config: BaseConfig):
        name = split_av_name(section)
        if not name:
            raise ValueError("AV name is required")

        super().__init__(config, section=section)
        self._name = name

    @classmethod
    def from_name(cls, name: str, config: BaseConfig):
        return cls(section=join_av_section_name(name), config=config)

    @property
    def name(self) -> str:
        return self._name

    @property
    def opened(self) -> bool:
        return self.get(self.K.opened, False)

    @opened.setter
    def opened(self, value: bool) -> None:
        self.set(self.K.opened, value)

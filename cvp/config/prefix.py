# -*- coding: utf-8 -*-

from typing import List

from cvp.config._base import BaseConfig


class SectionPrefix:
    def __init__(self, config: BaseConfig, prefix: str):
        self._config = config
        self._prefix = prefix

    @property
    def prefix(self) -> str:
        return self._prefix

    def _section_filter(self, key: str) -> bool:
        return key.startswith(self._prefix)

    def sections(self) -> List[str]:
        return list(filter(self._section_filter, self._config.sections()))

    def join_section_name(self, name: str) -> str:
        return f"{self._prefix}{name}"

    def split_section_name(self, name: str) -> str:
        if not name.startswith(self._prefix):
            raise ValueError(f"'{name}' does not start with '{self._prefix}'")

        begin_index = len(self._prefix)
        return name[begin_index:]

    def add_section(self, name: str) -> None:
        self._config.add_section(self.join_section_name(name))

# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Tuple

from cvp.config._base import BaseConfig, ValueT
from cvp.strings.case_converter import camelcase_to_snakecase


class BaseSection:
    @classmethod
    def auto_section_name(cls) -> str:
        return camelcase_to_snakecase(cls.__name__.removesuffix("Section"))

    def __init__(self, config: BaseConfig, section: Optional[str] = None):
        self._config = config
        self._section = section if section else self.auto_section_name()

    @property
    def section(self) -> str:
        return self._section

    def options(self) -> List[str]:
        return self._config.options(self._section)

    def keys(self) -> List[str]:
        return [option for option in self._config.options(self._section)]

    def items(self, *, raw=False) -> List[Tuple[str, str]]:
        return self._config.section_items(self._section, raw=raw)

    def clear(self):
        for option in self.options():
            self._config.remove_option(self._section, option)

    def dumps(self) -> Dict[str, str]:
        return {key: value for key, value in self.items(raw=True)}

    def extends(self, o: Dict[str, str]) -> None:
        for key, value in o.items():
            self._config.set(self._section, key, value)

    def has(self, key: str) -> bool:
        return self._config.has(self._section, key)

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseSection):
            return False
        return self.dumps() == other.dumps()

    def __bool__(self) -> bool:
        return bool(self._config.keys())

    def __contains__(self, item: str) -> bool:
        return self.has(item)

    def __iter__(self):
        return iter(self.items())

    def __len__(self):
        return len(self.keys())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get(self, key: str, default: ValueT, *, raw=False) -> ValueT:
        return self._config.get(self._section, key, default, raw=raw)

    def set(self, key: str, value: ValueT) -> None:
        self._config.set(self._section, key, value)

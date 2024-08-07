# -*- coding: utf-8 -*-

from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, Tuple, TypeVar, Union, overload

from cvp.types.string.to_boolean import string_to_boolean

_DefaultT = TypeVar("_DefaultT", str, bool, int, float)

SerializedConfig = Dict[str, List[Tuple[str, str]]]


def config_dumps(config: ConfigParser) -> SerializedConfig:
    result = dict()
    for section in config.sections():
        result[section] = [item for item in config.items(section)]
    return result


def config_loads(config: ConfigParser, o: SerializedConfig) -> None:
    for section, items in o.items():
        if not config.has_section(section):
            config.add_section(section)
        for option, value in items:
            config.set(section, option, value)


class BaseConfig:
    def __init__(self, filename: Optional[Union[str, PathLike]] = None):
        self._config = ConfigParser()
        if filename:
            self._config.read(filename)

    def sections(self):
        return self._config.sections()

    def clear(self) -> None:
        for section in self._config.sections():
            self._config.remove_section(section)

    def dumps(self) -> SerializedConfig:
        return config_dumps(self._config)

    def extends(self, o: Union["BaseConfig", ConfigParser, SerializedConfig]) -> None:
        if isinstance(o, BaseConfig):
            config_loads(self._config, o.dumps())
        elif isinstance(o, ConfigParser):
            config_loads(self._config, config_dumps(o))
        else:
            config_loads(self._config, o)

    def read(self, filename: Union[str, PathLike]) -> None:
        self._config.read(filename)

    def write(self, filename: Union[str, PathLike]) -> None:
        parent_dir = Path(filename).parent
        if not parent_dir.is_dir():
            parent_dir.mkdir(parents=True, exist_ok=True)
        with Path(filename).open("w") as fp:
            self._config.write(fp)

    def get_config_value(self, section: str, key: str, default=None) -> Optional[str]:
        if section not in self._config:
            return default
        if key not in self._config[section]:
            return default
        return self._config[section][key]

    def set_config_value(self, section: str, key: str, value: str) -> None:
        if section not in self._config:
            self._config[section] = dict()
        self._config[section][key] = value

    def has(self, section: str, key: str) -> bool:
        if section in self._config:
            return key in self._config[section]
        else:
            return False

    # fmt: off
    @overload
    def get(self, section: str, key: str) -> Optional[str]: ...
    @overload
    def get(self, section: str, key: str, default: str) -> str: ...
    @overload
    def get(self, section: str, key: str, default: bool) -> bool: ...
    @overload
    def get(self, section: str, key: str, default: int) -> int: ...
    @overload
    def get(self, section: str, key: str, default: float) -> float: ...
    # fmt: on

    def get(
        self,
        section: str,
        key: str,
        default: Optional[_DefaultT] = None,
    ) -> Optional[Union[str, bool, int, float]]:
        if default is None:
            return self.get_config_value(section, key)
        value = self.get_config_value(section, key)
        if value is None:
            return default
        elif isinstance(default, str):
            return value
        elif isinstance(default, bool):
            return string_to_boolean(value)
        elif isinstance(default, int):
            return int(value)
        elif isinstance(default, float):
            return float(value)
        else:
            raise TypeError(f"Unsupported default type: {type(default).__name__}")

    def set(self, section: str, key: str, value: _DefaultT) -> None:
        config_data = value if isinstance(value, str) else str(value)
        self.set_config_value(section, key, config_data)

# -*- coding: utf-8 -*-

from configparser import DEFAULTSECT, ConfigParser, ExtendedInterpolation
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union, overload

from cvp.system.environ_keys import CVP_HOME
from cvp.types.string.to_boolean import string_to_boolean
from cvp.variables import CONFIG_VALUE_SEPARATOR

ValueUnion = Union[
    str,
    bool,
    int,
    float,
    Sequence[str],
    Sequence[bool],
    Sequence[int],
    Sequence[float],
]
SerializedObject = Dict[str, Dict[str, str]]


def config_dumps(config: ConfigParser) -> SerializedObject:
    result = dict()
    for section in config.sections():
        result[section] = {key: value for key, value in config.items(section, raw=True)}
    return result


def config_loads(config: ConfigParser, o: SerializedObject) -> None:
    for section, items in o.items():
        if not config.has_section(section):
            config.add_section(section)
        for option, value in items.items():
            config.set(section, option, value)


class BaseConfig:
    _vars: Dict[str, str]

    def __init__(
        self,
        filename: Optional[Union[str, PathLike]] = None,
        cvp_home: Optional[str] = None,
        *,
        separator=CONFIG_VALUE_SEPARATOR,
    ):
        self._config = ConfigParser(
            defaults=None,
            dict_type=dict,
            allow_no_value=False,
            delimiters=("=",),
            comment_prefixes=("#",),
            inline_comment_prefixes=None,
            strict=True,
            empty_lines_in_values=False,
            default_section=DEFAULTSECT,
            interpolation=ExtendedInterpolation(),
        )
        self._vars = {CVP_HOME: cvp_home if cvp_home else str()}
        self._separator = separator
        if filename:
            self._config.read(filename)

    @property
    def vars(self):
        return self._vars

    @property
    def home(self):
        return self._vars

    def sections(self) -> List[str]:
        return self._config.sections()

    def options(self, section: str) -> List[str]:
        return self._config.options(section)

    def keys(self) -> List[Tuple[str, str]]:
        result = list()
        for section in self._config.sections():
            for option in self._config.options(section):
                result.append((section, option))
        return result

    def items(self, *, raw=False) -> List[Tuple[str, str, str]]:
        result = list()
        for section, option in self.keys():
            value = self._config.get(section, option, raw=raw, vars=self._vars)
            result.append((section, option, value))
        return result

    def section_items(self, section: str, *, raw=False) -> List[Tuple[str, str]]:
        result = list()
        for option in self.options(section):
            value = self._config.get(section, option, raw=raw, vars=self._vars)
            result.append((option, value))
        return result

    def clear(self) -> None:
        for section in self._config.sections():
            self._config.remove_section(section)

    def remove_section(self, section: str) -> bool:
        return self._config.remove_section(section)

    def remove_option(self, section: str, option: str) -> bool:
        return self._config.remove_option(section, option)

    def dumps(self) -> SerializedObject:
        return config_dumps(self._config)

    def extends(self, o: Union["BaseConfig", ConfigParser, SerializedObject]) -> None:
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

    def add_section(self, section: str) -> None:
        self._config.add_section(section)

    def set_config_value(
        self,
        section: str,
        key: str,
        value: Optional[str] = None,
    ) -> None:
        if section not in self._config:
            self._config.add_section(section)
        self._config.set(section, key, value)

    def has_section(self, section: str) -> bool:
        return self._config.has_section(section)

    def has_option(self, section: str, key: str) -> bool:
        return self._config.has_option(section, key)

    def has(self, section: str, key: Optional[str] = None) -> bool:
        if not self._config.has_section(section):
            return False
        assert section in self._config
        if not key:
            return True
        assert isinstance(key, str)
        return self.has_option(section, key)

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseConfig):
            return False
        return self.dumps() == other.dumps()

    def __bool__(self) -> bool:
        return bool(self._config.sections())

    def __contains__(self, item: Sequence[str]) -> bool:
        return self.has(item[0], item[1])

    def __iter__(self):
        return iter(self.items())

    def __len__(self):
        return len(self.keys())

    # fmt: off
    @overload
    def get(self, section: str, key: str, *, raw=False) -> Optional[str]: ...
    @overload
    def get(self, section: str, key: str, default: str, *, raw=False) -> str: ...
    @overload
    def get(self, section: str, key: str, default: bool, *, raw=False) -> bool: ...
    @overload
    def get(self, section: str, key: str, default: int, *, raw=False) -> int: ...
    @overload
    def get(self, section: str, key: str, default: float, *, raw=False) -> float: ...

    @overload
    def get(self, section: str, key: str, default: Sequence[str], *, raw=False) -> Sequence[str]: ...  # noqa: E501
    @overload
    def get(self, section: str, key: str, default: Sequence[bool], *, raw=False) -> Sequence[bool]: ...  # noqa: E501
    @overload
    def get(self, section: str, key: str, default: Sequence[int], *, raw=False) -> Sequence[int]: ...  # noqa: E501
    @overload
    def get(self, section: str, key: str, default: Sequence[float], *, raw=False) -> Sequence[float]: ...  # noqa: E501
    # fmt: on

    def get(
        self,
        section: str,
        key: str,
        default: Optional[ValueUnion] = None,
        *,
        raw=False,
    ) -> Optional[ValueUnion]:
        if not self._config.has_section(section):
            return default

        if not self._config.has_option(section, key):
            return default

        if default is None:
            return self._config.get(section, key, raw=raw, vars=self._vars)

        assert default is not None

        if isinstance(default, str):
            return self._config.get(section, key, raw=raw, vars=self._vars)

        elif isinstance(default, bool):
            _boolean_value = self._config.get(section, key, raw=raw, vars=self._vars)
            return string_to_boolean(_boolean_value)

        elif isinstance(default, int):
            return self._config.getint(section, key, raw=raw, vars=self._vars)

        elif isinstance(default, float):
            return self._config.getfloat(section, key, raw=raw, vars=self._vars)

        elif isinstance(default, Sequence):
            value = self._config.get(section, key, raw=raw, vars=self._vars)
            items = value.split(self._separator)
            if len(default) == 0:
                return tuple(items)
            elif isinstance(default[0], str):
                return tuple(item.strip() for item in items)
            elif isinstance(default[0], bool):
                return tuple(string_to_boolean(item.strip()) for item in items)
            elif isinstance(default[0], int):
                return tuple(int(item.strip()) for item in items)
            elif isinstance(default[0], float):
                return tuple(float(item.strip()) for item in items)

        raise TypeError(f"Unsupported default type: {type(default).__name__}")

    def encode_value(self, value: ValueUnion) -> str:
        if isinstance(value, str):
            return value
        elif isinstance(value, Sequence):
            match len(value):
                case 0:
                    return str()
                case 1:
                    return str(value[0])
                case x:
                    buffer = StringIO()
                    buffer.write(str(value[0]))
                    for i in range(1, x):
                        buffer.write(f"{self._separator}{value[i]}")
                    return buffer.getvalue()
        else:
            return str(value)

    def set(self, section: str, key: str, value: ValueUnion) -> None:
        self.set_config_value(section, key, self.encode_value(value))

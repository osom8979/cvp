# -*- coding: utf-8 -*-

import platform
from enum import StrEnum, unique
from typing import Final, Optional

_windows: Final[str] = "windows"
_linux: Final[str] = "linux"
_darwin: Final[str] = "darwin"

_x64: Final[str] = "x64"
_x86: Final[str] = "x86"
_arm64: Final[str] = "arm64"


@unique
class SysMach(StrEnum):
    windows_x64 = f"{_windows}.{_x64}"
    windows_x86 = f"{_windows}.{_x86}"
    windows_arm64 = f"{_windows}.{_arm64}"

    linux_x64 = f"{_linux}.{_x64}"
    linux_x86 = f"{_linux}.{_x86}"
    linux_arm64 = f"{_linux}.{_arm64}"

    darwin_x64 = f"{_darwin}.{_x64}"
    darwin_x86 = f"{_darwin}.{_x86}"
    darwin_arm64 = f"{_darwin}.{_arm64}"  # Apple Silicon ARM


def get_normalized_system(system: Optional[str] = None) -> str:
    system = system if system else platform.system()
    assert system is not None

    match system:
        case "Darwin":
            return _darwin
        case "Windows":
            return _windows
        case "Linux":
            return _linux
        case sys:
            raise ValueError(f"Unsupported platform: {sys}")


def get_normalized_machine(machine: Optional[str] = None) -> str:
    machine = machine if machine else platform.machine()
    assert machine is not None

    match machine:
        case "x86_64":
            return _x64
        case "i386":
            return _x86
        case m if m in ("arm64", "aarch64"):
            return _arm64
        case m:
            raise ValueError(f"Unsupported machine: {m}")


def get_system_machine(
    system: Optional[str] = None,
    machine: Optional[str] = None,
) -> SysMach:
    system = system if system else get_normalized_system()
    machine = machine if machine else get_normalized_machine()
    assert system is not None
    assert machine is not None
    return SysMach(f"{system}.{machine}")

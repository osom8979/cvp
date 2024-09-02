# -*- coding: utf-8 -*-

from enum import StrEnum, unique

# noinspection PyProtectedMember
from psutil._common import (
    STATUS_DEAD,
    STATUS_DISK_SLEEP,
    STATUS_IDLE,
    STATUS_LOCKED,
    STATUS_PARKED,
    STATUS_RUNNING,
    STATUS_SLEEPING,
    STATUS_STOPPED,
    STATUS_SUSPENDED,
    STATUS_TRACING_STOP,
    STATUS_WAITING,
    STATUS_WAKE_KILL,
    STATUS_WAKING,
    STATUS_ZOMBIE,
)


@unique
class ProcessStatusEx(StrEnum):
    running = STATUS_RUNNING
    sleeping = STATUS_SLEEPING
    disk_sleep = STATUS_DISK_SLEEP
    stopped = STATUS_STOPPED
    tracing_stop = STATUS_TRACING_STOP
    zombie = STATUS_ZOMBIE
    dead = STATUS_DEAD
    wake_kill = STATUS_WAKE_KILL
    waking = STATUS_WAKING
    idle = STATUS_IDLE  # Linux, macOS, FreeBSD
    locked = STATUS_LOCKED  # FreeBSD
    waiting = STATUS_WAITING  # FreeBSD
    suspended = STATUS_SUSPENDED  # NetBSD
    parked = STATUS_PARKED  # Linux
    no_such = "no-such"  # psutil.NoSuchProcess
    not_exists = "not-exists"  # IndexError
    exited = "exited"

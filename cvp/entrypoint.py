# -*- coding: utf-8 -*-

from sys import exit as sys_exit
from typing import List, Optional

from cvp.apps import run_app
from cvp.arguments import CMDS, DEFAULT_CMD, get_default_arguments


def main(cmdline: Optional[List[str]] = None) -> int:
    args = get_default_arguments(cmdline)

    if not args.cmd:
        args.cmd = DEFAULT_CMD

    assert args.cmd in CMDS
    return run_app(args.cmd, args)


if __name__ == "__main__":
    sys_exit(main())

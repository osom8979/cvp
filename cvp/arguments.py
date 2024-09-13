# -*- coding: utf-8 -*-

from argparse import REMAINDER, ArgumentParser, Namespace, RawDescriptionHelpFormatter
from functools import lru_cache
from os import R_OK, access, getcwd
from os.path import isfile, join
from typing import Final, List, Optional, Sequence

from cvp.system.environ import get_typed_environ_value as get_eval
from cvp.system.environ_keys import (
    CVP_DOTENV_PATH,
    CVP_HOME,
    CVP_NO_DOTENV,
    CVP_USE_UVLOOP,
)
from cvp.variables import DEFAULT_CVP_HOME_PATH, LOCAL_DOTENV_FILENAME

PROG: Final[str] = "cvp"
DESCRIPTION: Final[str] = "Computer Vision Player"
EPILOG: Final[str] = ""

CMD_PLAYER: Final[str] = "player"
CMD_PLAYER_HELP: Final[str] = "Desktop GUI"
CMD_PLAYER_EPILOG = f"""
Simply usage:
  {PROG} {CMD_PLAYER}
"""

CMD_WORKER: Final[str] = "worker"
CMD_WORKER_HELP: Final[str] = "Background Worker"
CMD_WORKER_EPILOG = f"""
Simply usage:
  {PROG} {CMD_WORKER}
"""

CMDS: Final[Sequence[str]] = CMD_PLAYER, CMD_WORKER
DEFAULT_CMD: Final[str] = CMD_PLAYER


@lru_cache
def version() -> str:
    # [IMPORTANT] Avoid 'circular import' issues
    from cvp import __version__

    return __version__


def add_dotenv_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--no-dotenv",
        action="store_true",
        default=get_eval(CVP_NO_DOTENV, False),
        help="Do not use dot-env file",
    )
    parser.add_argument(
        "--dotenv-path",
        default=get_eval(CVP_DOTENV_PATH, join(getcwd(), LOCAL_DOTENV_FILENAME)),
        metavar="file",
        help=f"Specifies the dot-env file (default: '{LOCAL_DOTENV_FILENAME}')",
    )


def add_player_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_PLAYER,
        help=CMD_PLAYER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_PLAYER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)


def add_worker_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_WORKER,
        help=CMD_WORKER_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_WORKER_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)

    parser.add_argument(
        "--use-uvloop",
        action="store_true",
        default=get_eval(CVP_USE_UVLOOP, False),
        help="Replace the event loop with uvloop",
    )
    parser.add_argument(
        "opts",
        nargs=REMAINDER,
        help="Worker pipeline arguments",
    )


def default_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROG,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )

    add_dotenv_arguments(parser)

    parser.add_argument(
        "--home",
        metavar="dir",
        default=get_eval(CVP_HOME, DEFAULT_CVP_HOME_PATH),
        help=f"{PROG}'s home directory (default: '{DEFAULT_CVP_HOME_PATH}')",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=version(),
    )

    subparsers = parser.add_subparsers(dest="cmd")
    add_player_parser(subparsers)
    add_worker_parser(subparsers)

    return parser


def _load_dotenv(
    cmdline: Optional[List[str]] = None,
    namespace: Optional[Namespace] = None,
) -> None:
    parser = ArgumentParser(add_help=False, allow_abbrev=False, exit_on_error=False)
    add_dotenv_arguments(parser)
    args = parser.parse_known_args(cmdline, namespace)[0]

    assert isinstance(args.no_dotenv, bool)
    assert isinstance(args.dotenv_path, str)

    if args.no_dotenv:
        return
    if not isfile(args.dotenv_path):
        return
    if not access(args.dotenv_path, R_OK):
        return

    try:
        from dotenv import load_dotenv

        load_dotenv(args.dotenv_path)
    except ModuleNotFoundError:
        pass


def _remove_dotenv_attrs(namespace: Namespace) -> Namespace:
    assert isinstance(namespace.no_dotenv, bool)
    assert isinstance(namespace.dotenv_path, str)

    del namespace.no_dotenv
    del namespace.dotenv_path

    assert not hasattr(namespace, "no_dotenv")
    assert not hasattr(namespace, "dotenv_path")

    return namespace


def get_default_arguments(
    cmdline: Optional[List[str]] = None,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    # [IMPORTANT] Dotenv related options are processed first.
    _load_dotenv(cmdline, namespace)

    parser = default_argument_parser()
    args = parser.parse_known_args(cmdline, namespace)[0]

    # Remove unnecessary dotenv attrs
    return _remove_dotenv_attrs(args)

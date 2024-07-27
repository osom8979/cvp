# -*- coding: utf-8 -*-

from argparse import Namespace


def player_main(args: Namespace) -> None:
    assert isinstance(args.imgui_ini, str)
    assert isinstance(args.player_ini, str)
    assert isinstance(args.colored_logging, bool)
    assert isinstance(args.default_logging, bool)
    assert isinstance(args.simple_logging, bool)
    assert isinstance(args.rotate_logging_prefix, str)
    assert isinstance(args.rotate_logging_when, str)
    assert isinstance(args.severity, str)
    assert isinstance(args.debug, bool)
    assert isinstance(args.verbose, int)
    assert isinstance(args.D, bool)

    from cvp.apps.player.context import PlayerContext

    context = PlayerContext(args)
    context.start()

# -*- coding: utf-8 -*-

from argparse import Namespace


def player_main(args: Namespace) -> None:
    from cvp.apps.player.context import PlayerContext

    context = PlayerContext.from_namespace(args)
    context.start()

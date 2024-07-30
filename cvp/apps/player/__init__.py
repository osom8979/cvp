# -*- coding: utf-8 -*-

from argparse import Namespace

from cvp.renderer.pygame import hide_pygame_prompt


def player_main(args: Namespace) -> None:
    hide_pygame_prompt()

    from cvp.apps.player.context import PlayerContext

    context = PlayerContext.from_namespace(args)
    context.start()

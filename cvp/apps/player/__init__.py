# -*- coding: utf-8 -*-

from argparse import Namespace

from cvp.context import Context
from cvp.renderer.pygame import hide_pygame_prompt


def player_main(args: Namespace) -> None:
    hide_pygame_prompt()

    context = Context.from_namespace(args)

    from cvp.apps.player.app import PlayerApplication

    PlayerApplication(context).start()

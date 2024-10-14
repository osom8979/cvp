# -*- coding: utf-8 -*-

from argparse import Namespace


def player_main(args: Namespace) -> None:
    from cvp.apps.player.app import PlayerApplication
    from cvp.context.context import Context
    from cvp.pygame.environ import hide_pygame_prompt

    hide_pygame_prompt()

    assert isinstance(args.home, str)
    context = Context(args.home)
    app = PlayerApplication(context)
    app.start()

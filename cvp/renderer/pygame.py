# -*- coding: utf-8 -*-

from cvp.system.environ import exchange_env_context


def hide_pygame_prompt() -> None:
    with exchange_env_context("PYGAME_HIDE_SUPPORT_PROMPT", "hide"):
        import pygame  # noqa: F401

# -*- coding: utf-8 -*-

from logging import Logger


async def shield_any(coro, logger: Logger):
    try:
        return await coro
    except BaseException as e:
        # Shields user-raised exceptions
        logger.exception(e)

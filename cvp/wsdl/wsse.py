# -*- coding: utf-8 -*-

from typing import Optional

from zeep.wsse import UsernameToken


def create_username_token(
    username: Optional[str],
    password: Optional[str],
    use_digest=False,
) -> Optional[UsernameToken]:
    if not username:
        return None
    if not password:
        return None
    return UsernameToken(username=username, password=password, use_digest=use_digest)

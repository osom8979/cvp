# -*- coding: utf-8 -*-

from typing import Deque

from cvp.msgs.msg import Msg


class MsgQueue(Deque[Msg]):
    def get(self):
        result = list()
        while True:
            try:
                result.append(self.popleft())
            except IndexError:
                break
        return result

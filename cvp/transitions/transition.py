# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional, Sequence, Tuple, Union
from weakref import ReferenceType, ref

from cvp.transitions.easing import EasingCallable, linear


class TransitionProp:
    def __init__(self, start: Optional[float], end: float):
        self.start = start
        self.end = end

    @classmethod
    def from_value(cls, value: Union[float, Tuple[float, float], "TransitionProp"]):
        if isinstance(value, cls):
            return cls(value.start, value.end)

        if isinstance(value, Sequence):
            if len(value) == 2:
                return cls(value[0], value[1])
            else:
                raise ValueError("The length of the prop value must be 2")

        if isinstance(value, float):
            return cls(None, value)
        if isinstance(value, int):
            return cls(None, float(value))

        raise TypeError(f"Unexpected prop value type: {type(value).__name__}")

    def update_start(self, obj: Any, key: str, default=0.0) -> None:
        assert not isinstance(obj, ReferenceType)
        value = getattr(obj, key, default)
        value = value if value is not None else default
        assert value is not None
        self.start = value


class Transition:
    def __init__(
        self,
        obj: Any,
        props: Dict[str, Union[float, Tuple[float, float], TransitionProp]],
        easing: EasingCallable = linear,
        duration=1.0,
        delay=0.0,
        loop=False,
        update_start_props_if_none=True,
        *,
        play=True,
        elapsed=0.0,
        done=False,
    ):
        if obj is None:
            raise ValueError("Object cannot be None")

        self._ref = obj if isinstance(obj, ReferenceType) else ref(obj)
        self._props = {k: TransitionProp.from_value(v) for k, v in props.items()}
        self._easing = easing
        self._duration = duration
        self._delay = delay
        self._loop = loop
        self._play = play
        self._elapsed = elapsed
        self._done = done

        if update_start_props_if_none:
            self.update_start_props_if_none()

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result._ref = self._ref
        result._props = {
            k: TransitionProp.from_value(v) for k, v in self._props.items()
        }
        result._easing = self._easing
        result._duration = self._duration
        result._delay = self._delay
        result._loop = self._loop
        result._play = self._play
        result._elapsed = self._elapsed
        result._done = self._done
        return result

    def copy(self):
        return self.__copy__()

    @property
    def done(self):
        return self._done

    @property
    def ref(self):
        return self._ref

    @property
    def obj(self):
        return self._ref()

    @obj.setter
    def obj(self, obj: Any):
        self._ref = obj if isinstance(obj, ReferenceType) else ref(obj)

    def update_start_props(self):
        obj = self.obj
        if obj is not None:
            for key, value in self._props.items():
                value.update_start(obj, key)

    def update_start_props_if_none(self):
        obj = self.obj
        if obj is not None:
            for key, value in self._props.items():
                if value.start is None:
                    value.update_start(obj, key)

    def start(self):
        self._play = True

    def stop(self):
        self._play = False

    def reset(self):
        self._play = False
        self._elapsed = 0.0
        self._done = False

    def update(self, tick: int) -> bool:
        """Update the next values.

        :param tick: milliseconds time used in the previous tick.
        :return: Returns whether the update is complete.
        """

        if self._play:
            self._elapsed += tick / 1000.0

        if self._done:
            return True

        if self._elapsed < self._delay:
            return False

        elapsed = self._elapsed - self._delay
        assert 0 <= elapsed

        if self._loop:
            step = elapsed / self._duration
            self._done = False
        else:
            step = min(elapsed / self._duration, 1.0)
            assert 0.0 <= step <= 1.0
            self._done = step == 1.0

        if self._play:
            obj = self.obj
            if obj is not None:
                for key, value in self._props.items():
                    if value.start is None:
                        value.update_start(obj, key)
                    delta = value.end - value.start
                    next_value = self._easing(step) * delta + value.start
                    setattr(obj, key, next_value)

        return self._done

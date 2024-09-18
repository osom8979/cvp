# -*- coding: utf-8 -*-

from collections import deque
from inspect import Parameter, Signature
from inspect import signature as _inspect_signature
from typing import Any, Callable, Dict, Sequence, Union


def _assert_parameter_kind_order(sig: Signature) -> None:
    # [IMPORTANT]
    # Support comparison and ordering, in the following order
    pass_positional_only = False
    pass_positional_or_keyword = False
    pass_var_positional = False
    pass_keyword_only = False
    # 'pass_var_keyword' is always False, so it was removed.

    for param in deque(sig.parameters.values()):
        if param.kind == Parameter.POSITIONAL_ONLY:
            assert not pass_positional_only
            assert not pass_positional_or_keyword
            assert not pass_var_positional
            assert not pass_keyword_only
            continue

        if param.kind == Parameter.POSITIONAL_OR_KEYWORD:
            pass_positional_only = True
            assert not pass_positional_or_keyword
            assert not pass_var_positional
            assert not pass_keyword_only
            continue

        if param.kind == Parameter.VAR_POSITIONAL:
            pass_positional_only = True
            pass_positional_or_keyword = True
            assert not pass_var_positional
            assert not pass_keyword_only
            continue

        if param.kind == Parameter.KEYWORD_ONLY:
            pass_positional_only = True
            pass_positional_or_keyword = True
            pass_var_positional = True
            assert not pass_keyword_only
            continue

        if param.kind == Parameter.VAR_KEYWORD:
            pass_positional_only = True
            pass_positional_or_keyword = True
            pass_var_positional = True
            pass_keyword_only = True
            continue

        assert False, f"Unexpected parameter kind: {param.kind}"


def assert_parameter_kind_order(sig_or_func: Union[Signature, Callable]) -> None:
    if isinstance(sig_or_func, Signature):
        _assert_parameter_kind_order(sig_or_func)
    else:
        _assert_parameter_kind_order(_inspect_signature(sig_or_func))


class BindCallable:
    def __init__(
        self,
        func: Callable,
        signature: Signature,
        args: Sequence[Any],
        kwargs: Dict[str, Any],
    ):
        self.func = func
        self.signature = signature
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


def force_bind(func: Callable, *args, **kwargs) -> BindCallable:
    """
    Bind parameters so that the function is called even if the argument is incorrect.
    """

    sig = _inspect_signature(func)

    provided_args = deque(args)
    provided_kwargs = kwargs.copy()

    bind_args = list()
    bind_kwargs = dict()

    for param in sig.parameters.values():
        if param.kind == Parameter.POSITIONAL_ONLY:
            if provided_args:
                bind_args.append(provided_args.popleft())
            elif param.default != Parameter.empty:
                bind_args.append(param.default)
            else:
                bind_args.append(None)
            continue

        if param.kind == Parameter.POSITIONAL_OR_KEYWORD:
            if param.name in provided_kwargs:
                bind_args.append(provided_kwargs.pop(param.name))
            elif provided_args:
                bind_args.append(provided_args.popleft())
            elif param.default != Parameter.empty:
                bind_args.append(param.default)
            else:
                bind_args.append(None)
            continue

        if param.kind == Parameter.VAR_POSITIONAL:
            while provided_args:
                bind_args.append(provided_args.popleft())
            continue

        if param.kind == Parameter.KEYWORD_ONLY:
            if param.name in provided_kwargs:
                bind_kwargs[param.name] = provided_kwargs.pop(param.name)
            elif param.default != Parameter.empty:
                bind_kwargs[param.name] = param.default
            else:
                bind_kwargs[param.name] = None
            continue

        if param.kind == Parameter.VAR_KEYWORD:
            while provided_kwargs:
                name, value = provided_kwargs.popitem()
                bind_kwargs[name] = value
            continue

        assert False, f"Unexpected parameter kind: {param.kind}"

    return BindCallable(func, sig, bind_args, bind_kwargs)

# -*- coding: utf-8 -*-

try:
    # noinspection PyUnresolvedReferences
    import pydevd_pycharm
except ImportError:
    pass


def pydevd_pycharm_set_trace(
    host="localhost",
    port=5678,
    stdout_to_server=True,
    stderr_to_server=True,
):
    pydevd_pycharm.settrace(
        host=host,
        stdoutToServer=stdout_to_server,
        stderrToServer=stderr_to_server,
        port=port,
        suspend=True,
        trace_only_current_thread=False,
        overwrite_prev_trace=False,
        patch_multiprocessing=False,
        stop_at_frame=None,
    )

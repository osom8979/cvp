# -*- coding: utf-8 -*-

from argparse import Namespace


def worker_main(args: Namespace) -> None:
    from cvp.apps.worker.app import WorkerApplication

    WorkerApplication.from_namespace(args).start()

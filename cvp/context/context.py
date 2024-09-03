# -*- coding: utf-8 -*-

import os
from os import PathLike
from threading import Event
from typing import Optional, Union

from cvp.config.config import Config
from cvp.filesystem.permission import test_directory, test_readable
from cvp.logging.logging import (
    convert_level_number,
    dumps_default_logging_config,
    loads_logging_config,
    logger,
    set_root_level,
)
from cvp.process.manager import ProcessManager
from cvp.resources.home import HomeDir


class Context:
    def __init__(self, home: Optional[Union[str, PathLike[str]]] = None):
        self._home = HomeDir.from_path(home)
        self._done = Event()

        test_directory(self._home)
        test_readable(self._home)

        self._readonly = not os.access(self._home, os.W_OK)
        if self._readonly:
            logger.warning("Runs in read-only mode")

        if not self._readonly and not self._home.exists():
            logger.info(f"Create home directory: '{str(self._home)}'")
            self._home.mkdir(parents=True, exist_ok=True)

        self._config = Config(self._home.cvp_ini, self._home)

        logging_config_path = self._config.logging.config_path
        if os.path.isfile(logging_config_path):
            loads_logging_config(logging_config_path)
            logger.info(f"Loads the logging config file: '{logging_config_path}'")

        root_severity = self._config.logging.root_severity
        if root_severity:
            level = convert_level_number(root_severity)
            set_root_level(level)
            logger.log(level, f"Changed root severity: {root_severity}")

        thread_workers = self._config.concurrency.thread_workers
        process_workers = self._config.concurrency.process_workers
        self._pm = ProcessManager(
            self._config.ffmpeg,
            home=self._home,
            thread_workers=thread_workers,
            process_workers=process_workers,
        )

    @property
    def readonly(self):
        return self._readonly

    @property
    def home(self):
        return self._home

    @property
    def config(self):
        return self._config

    @property
    def pm(self):
        return self._pm

    @property
    def debug(self) -> bool:
        return self._config.debug

    @property
    def verbose(self) -> int:
        return self._config.verbose

    def quit(self) -> None:
        self._done.set()

    def is_done(self) -> bool:
        return self._done.is_set()

    def teardown(self) -> None:
        self._pm.teardown(self._config.processes.teardown_timeout)

        if self._readonly:
            logger.warning("Runs in read-only mode")
            return

        if not self._home.is_dir():
            logger.info(f"Create home directory: '{str(self._home)}'")
            self._home.mkdir(parents=True, exist_ok=True)

            if not self._home.is_dir():
                logger.error(f"Home is not a directory type: '{str(self._home)}'")
                return

        if not os.access(self._home, os.W_OK):
            logger.error(f"No write permission in home directory: '{str(self._home)}'")
            return

        self._config.write(self._home.cvp_ini)

        if not self._home.logging_json.exists():
            logging_config_path = str(self._home.logging_json)
            logger.debug(f"Save the default log config file: '{logging_config_path}'")
            logging_json = dumps_default_logging_config(cvp_home=self._home)
            self._home.logging_json.write_text(logging_json)

# -*- coding: utf-8 -*-

import os
from os import PathLike
from threading import Event
from typing import Optional, Union

from cvp.config.config import Config
from cvp.filesystem.permission import test_directory, test_readable, test_writable
from cvp.flow.manager import FlowManager
from cvp.logging.logging import (
    convert_level_number,
    dumps_default_logging_config,
    loads_logging_config,
    logger,
    set_root_level,
)
from cvp.process.manager import ProcessManager
from cvp.resources.download.archive import DownloadArchive
from cvp.resources.download.links.tuples import LinkInfo
from cvp.resources.download.runner import DownloadRunner
from cvp.resources.home import HomeDir
from cvp.system.environ_keys import PYOPENGL_USE_ACCELERATE, SDL_VIDEO_X11_FORCE_EGL


class Context:
    def __init__(self, home: Union[str, PathLike[str]]):
        test_directory(home)
        test_readable(home)
        test_writable(home)

        self._home = HomeDir(home)
        self._config = Config()
        self._done = Event()

        if not self._home.exists():
            logger.info(f"Create home directory: '{str(self._home)}'")
            self._home.mkdir(parents=True, exist_ok=True)

        if self._home.cvp_yml.is_file():
            self._config.read_yaml(self._home.cvp_yml)

        if not self._home.logging_json.exists():
            self.save_logging_config()
        if not self._config.logging.config_path:
            logging_config_path = str(self._home.logging_json)
            self._config.logging.config_path = logging_config_path
            logger.info(f"Initialize logging config file: '{logging_config_path}'")

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
        self._process_manager = ProcessManager(
            config=self._config.ffmpeg,
            home=self._home,
            thread_workers=thread_workers,
            process_workers=process_workers,
        )

        if self.config.graphic.force_egl is not None:
            force_egl = self.config.graphic.force_egl_environ
            os.environ[SDL_VIDEO_X11_FORCE_EGL] = force_egl
            logger.info(f"Update environ: {SDL_VIDEO_X11_FORCE_EGL}={force_egl}")

        if self.config.graphic.use_accelerate is not None:
            use_accelerate = self.config.graphic.use_accelerate_environ
            os.environ[PYOPENGL_USE_ACCELERATE] = use_accelerate
            logger.info(f"Update environ: {PYOPENGL_USE_ACCELERATE}={use_accelerate}")

        self._flow_manager = FlowManager()
        self.refresh_flow_graphs()

    @property
    def home(self):
        return self._home

    @property
    def config(self):
        return self._config

    @property
    def pm(self):
        return self._process_manager

    @property
    def fm(self):
        return self._flow_manager

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

    def make_downloader(self, link: LinkInfo):
        return DownloadArchive.from_link(
            link=link,
            extract_root=self._home,
            cache_dir=self._home.cache,
            temp_dir=self._home.temp,
        )

    def start_download_thread(
        self,
        downloader: DownloadArchive,
        download_timeout: Optional[float] = None,
        verify_checksum=True,
    ):
        return DownloadRunner(
            executor=self._process_manager.thread_pool,
            downloader=downloader,
            download_timeout=download_timeout,
            verify_checksum=verify_checksum,
        )

    def teardown(self) -> None:
        self._process_manager.teardown(self._config.process_manager.teardown_timeout)

    def validate_writable_home(self) -> None:
        if not self._home.is_dir():
            logger.debug(f"Create home directory: '{str(self._home)}'")
            self._home.mkdir(parents=True, exist_ok=True)

            if not self._home.is_dir():
                raise NotADirectoryError(
                    f"Home is not a directory type: '{str(self._home)}'"
                )

        if not os.access(self._home, os.W_OK):
            raise PermissionError(
                f"No write permission in home directory: '{str(self._home)}'"
            )

    def save_config_unsafe(self) -> None:
        config_path = self._home.cvp_yml
        logger.info(f"Save the config file: '{str(config_path)}'")
        self._config.write_yaml(config_path)

    def save_config(self) -> None:
        try:
            self.validate_writable_home()
        except BaseException as e:
            logger.error(e)
        else:
            self.save_config_unsafe()

    def save_logging_config_unsafe(self) -> None:
        logging_json = dumps_default_logging_config(cvp_home=self._home)
        logging_config_path = str(self._home.logging_json)
        logger.info(f"Save the default logging config file: '{logging_config_path}'")
        self._home.logging_json.write_text(logging_json)

    def save_logging_config(self) -> None:
        try:
            self.validate_writable_home()
        except BaseException as e:
            logger.error(e)
        else:
            self.save_logging_config_unsafe()

    def refresh_flow_graphs(self):
        for file in self._home.flows.find_graph_files():
            self._flow_manager.update_graph_yaml(file)

# -*- coding: utf-8 -*-

import os
from http import HTTPStatus
from http.client import HTTPResponse
from shutil import move, unpack_archive
from tempfile import TemporaryDirectory
from typing import Final, List, NamedTuple, Optional, Sequence, Tuple, Union
from urllib.parse import ParseResult, urlparse, urlunparse
from urllib.request import urlopen

from cvp.assets import get_assets_dir, get_cache_dir
from cvp.hashfunc.checksum import Method
from cvp.hashfunc.checksum import checksum as calc_checksum

DEFAULT_DOWNLOAD_TIMEOUT: Final[float] = 30.0


class ExtractPath(NamedTuple):
    archive_path: str
    extract_path: str


class Checksum(NamedTuple):
    hash_method: Method
    hash_value: str

    @classmethod
    def parse(cls, method_value: str, delimiter=":"):
        method, value = method_value.split(delimiter, 1)
        assert isinstance(method, str)
        assert isinstance(value, str)
        return cls(Method(method.strip().lower()), value.strip())


class DownloadArchive:
    _url: str
    _components: ParseResult
    _paths: List[ExtractPath]
    _checksum: Optional[Checksum]

    def __init__(
        self,
        url: Union[str, ParseResult],
        paths: Sequence[Union[Tuple[str, str], ExtractPath]],
        checksum: Optional[Union[str, Tuple[str, str], Checksum]] = None,
    ):
        if not paths:
            raise ValueError("No paths given")

        if isinstance(url, ParseResult):
            self._url = str(urlunparse(url))
            self._components = url
        else:
            assert isinstance(url, str)
            self._url = url
            self._components = urlparse(url)

        self._paths = list()
        for path in paths:
            if isinstance(path, ExtractPath):
                self._paths.append(path)
            else:
                assert isinstance(path, tuple)
                assert len(path) == 2
                assert isinstance(path[0], str)
                assert isinstance(path[1], str)
                self._paths.append(ExtractPath(path[0], path[1]))

        if checksum:
            if isinstance(checksum, Checksum):
                self._checksum = checksum
            elif isinstance(checksum, tuple):
                assert len(checksum) == 2
                assert isinstance(checksum[0], str)
                assert isinstance(checksum[1], str)
                self._checksum = Checksum(Method(checksum[0].lower()), checksum[1])
            else:
                self._checksum = Checksum.parse(checksum.strip())
        else:
            self._checksum = None

    def __repr__(self):
        return f"<DownloadArchive {self._url}>"

    @property
    def has_path(self) -> bool:
        return bool(self._paths)

    @property
    def has_checksum(self) -> bool:
        return self._checksum is not None

    @property
    def url(self) -> str:
        return self._url

    @property
    def paths(self):
        return self._paths

    @property
    def extract_files(self) -> List[str]:
        return [os.path.join(get_assets_dir(), p.extract_path) for p in self._paths]

    @property
    def has_extract_files(self):
        return all((os.path.isfile(p) for p in self.extract_files))

    @property
    def root_url(self) -> str:
        return f"{self._components.scheme}://{self._components.netloc}/"

    @property
    def filename(self) -> str:
        return os.path.basename(self._components.path)

    @property
    def cache_path(self) -> str:
        return os.path.join(get_cache_dir(), self.filename)

    def healthcheck(
        self,
        timeout: Optional[float] = None,
        status: Sequence[Union[int, HTTPStatus]] = (HTTPStatus.OK,),
    ) -> bool:
        with urlopen(self.root_url, timeout=timeout) as response:
            assert isinstance(response, HTTPResponse)
            return response.status in status

    def download_archive(self, timeout: Optional[float] = None) -> None:
        with urlopen(self._url, timeout=timeout) as response:
            with open(self.cache_path, "wb") as f:
                f.write(response.read())

    def verify_checksum(self) -> bool:
        if not self._checksum:
            raise ValueError("Checksum cache is empty")

        with open(self.cache_path, "rb") as f:
            method = self._checksum.hash_method
            value = self._checksum.hash_value
            return calc_checksum(method, f.read()) == value

    def extract(self) -> None:
        with TemporaryDirectory() as tmpdir:
            unpack_archive(self.cache_path, tmpdir)

            for path in self._paths:
                src = os.path.join(tmpdir, path.archive_path)
                dest = os.path.join(get_assets_dir(), path.extract_path)
                move(src, dest)

    def prepare(
        self,
        timeout: Optional[float] = DEFAULT_DOWNLOAD_TIMEOUT,
        verify_checksum=True,
    ) -> None:
        assert self.paths

        if self.has_extract_files:
            return

        if not os.path.isfile(self.cache_path):
            self.download_archive(timeout=timeout)

        if not os.path.isfile(self.cache_path):
            raise FileNotFoundError("Not found cache file")

        if verify_checksum and not self.verify_checksum():
            raise ValueError("Invalid checksum")

        self.extract()

        for path in self.extract_files:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"'{path}' is not a file")

import concurrent.futures
import pathlib
from collections.abc import Iterator
from logging import getLogger
from pathlib import Path
from typing import Type

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

from src.domain.interfaces import ILoader

logger = getLogger(__name__)


class DocumentLoader(ILoader):
    def __init__(
        self,
        paths: tuple[Path],
        glob: list[str],
        recursive: bool = False,
        loader_cls: Type[TextLoader] | None = None,
        use_multithreading: bool = False,
        workers: int = 4,
    ):
        self.paths = paths
        self.glob = glob
        self.loader_cls = loader_cls or TextLoader
        self.recursive = recursive
        self.use_multithreading = use_multithreading
        self.workers = workers

    def lazy_load(self) -> Iterator[Document]:
        if self.use_multithreading:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.workers
            ) as pool:
                futures = [
                    pool.submit(self._lazy_load_file, path) for path in self.file_paths
                ]

                for tasks in concurrent.futures.as_completed(futures):
                    for task in tasks.result():
                        yield task
        else:
            for path in self.file_paths:
                yield from self._lazy_load_file(path)

    def _lazy_load_file(self, path: pathlib.Path) -> Iterator[Document]:
        loader = self.loader_cls(path, encoding="utf-8", autodetect_encoding=True)
        for subdoc in loader.lazy_load():
            yield subdoc

    @property
    def file_paths(self):
        for path in self.paths:
            if not path.exists():
                raise FileNotFoundError(f"Path not found {path}")
            if path.is_file():
                yield path
            for pattern in self.glob:
                yield from path.rglob(pattern) if self.recursive else path.glob(pattern)

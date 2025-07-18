from abc import ABC, abstractmethod
from typing import Iterable, Iterator, List, Protocol

from langchain_core.documents import Document


class ILoader(ABC):
    @abstractmethod
    def lazy_load(self) -> Iterator[Document]: ...


class DocumentSplitter(Protocol):
    def split_documents(self, documents: Iterable[Document]) -> List[Document]: ...


class VectorStore(Protocol):
    def add_documents(self, documents: list[Document], **kwargs) -> list[str]: ...
    def update_documents(self, ids: list[str], documents: list[Document]) -> None: ...


class Cache(ABC):
    @abstractmethod
    def load(self) -> dict[str, str]: ...
    @abstractmethod
    def save(self, id_map: dict[str, str]): ...

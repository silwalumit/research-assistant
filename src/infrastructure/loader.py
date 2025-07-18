from collections.abc import Iterator

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


class IncrementalTextLoader(TextLoader):
    def lazy_load(self) -> Iterator[Document]: ...

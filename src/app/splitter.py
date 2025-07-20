import copy
import uuid
from logging import getLogger
from typing import Callable, Iterable, Iterator

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.shared.helpers import gen_hash

logger = getLogger()


class RecursiveTextSplitterWithHash(RecursiveCharacterTextSplitter):
    def __init__(
        self,
        enable_hash: bool = False,
        hasher: Callable[[str, int], str] = gen_hash,
        hasher_kwargs: dict | None = None,
        **kwargs,
    ):
        self._enable_hash = enable_hash
        self._hash_func: Callable = hasher
        self._hasher_kwargs = hasher_kwargs or {}
        super().__init__(**kwargs)

    def lazy_split_documents(self, documents: Iterable[Document]) -> Iterator[Document]:
        """Generate document chunks."""

        for document in documents:
            index = 0
            previous_chunk_len = 0
            text = document.page_content

            logger.info(f"Create document chunks for `{document.metadata['source']}`")
            for chunk in self.split_text(text):
                metadata = copy.deepcopy(document.metadata)
                if self._enable_hash:
                    text_hash = self._hash_func(chunk, **self._hasher_kwargs)
                    metadata["hash"] = text_hash

                if self._add_start_index:
                    offset = index + previous_chunk_len - self._chunk_overlap
                    index = text.find(chunk, max(0, offset))
                    metadata["start_index"] = index
                    previous_chunk_len = len(chunk)

                logger.info(f"Created chunk with hash {metadata['hash']}")
                yield Document(
                    page_content=chunk,
                    metadata=metadata,
                    id=str(uuid.uuid5(uuid.NAMESPACE_X500, chunk)),
                )

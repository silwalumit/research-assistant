import copy
import uuid
from typing import Callable, List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.shared.helpers import gen_hash


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

    def create_documents(
        self,
        texts: List[str],
        metadatas: List[dict] | None = None,
    ) -> List[Document]:
        """Create documents from a list of texts."""
        _metadatas = metadatas or [{}] * len(texts)
        documents = []
        for i, text in enumerate(texts):
            index = 0
            previous_chunk_len = 0
            for chunk in self.split_text(text):
                metadata = copy.deepcopy(_metadatas[i])
                if self._add_start_index:
                    offset = index + previous_chunk_len - self._chunk_overlap
                    index = text.find(chunk, max(0, offset))
                    metadata["start_index"] = index
                    previous_chunk_len = len(chunk)

                if self._enable_hash:
                    metadata["hash"] = self._hash_func(chunk, **self._hasher_kwargs)

                new_doc = Document(
                    page_content=chunk,
                    metadata=metadata,
                    id=str(uuid.uuid5(uuid.NAMESPACE_X500, chunk)),
                )
                documents.append(new_doc)
        return documents

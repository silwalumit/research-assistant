from logging import getLogger
from typing import cast

from src.app.interfaces import Cache, DocumentSplitter, ILoader, VectorStore

logger = getLogger()


def ingest_documents(
    loader: ILoader,
    splitter: DocumentSplitter,
    vector_store: VectorStore,
    cache: Cache,
):
    documents = loader.lazy_load()
    id_map = cache.load()
    sub_docs = []

    # Filter incremental docs
    for doc in splitter.lazy_split_documents(documents):
        if id_map.get(cast(str, doc.id)):
            message = (
                doc.metadata["hash"]
                if "hash" in doc.metadata
                else doc.page_content[:10]
            )
            logger.info(f"Discarding chunk {message}")
            continue
        sub_docs.append(doc)
        id_map[doc.id] = doc.metadata["hash"]

    cache.save(id_map)

    return vector_store.add_documents(sub_docs) if sub_docs else []

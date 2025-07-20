import pathlib
import time
from logging import getLogger

import click
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.app.ingestor import ingest_documents
from src.app.loader import DocumentLoader
from src.app.splitter import RecursiveTextSplitterWithHash
from src.shared.json_cache import JsonCache

logger = getLogger()


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    pass


@cli.command(help="Ingest document in knowledge base")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(
        exists=True,
        path_type=pathlib.Path,
    ),
)
@click.option("-r", "--recursive", is_flag=True)
@click.option("-t", "--threads", default=0)
@click.option("-c", "--chunk_size", default=500)
@click.option("-o", "--chunk_overlap", default=100)
@click.option("-pd", "--persist_dir", default="./data/chroma")
@click.pass_context
def ingest(
    ctx: click.Context,
    recursive: bool,
    paths: tuple[pathlib.Path],
    threads: int,
    chunk_size: int,
    chunk_overlap: int,
    persist_dir: str,
):
    start_time = time.perf_counter()
    logger.info(f"Running ingestion pipeline, {paths=}")
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    doc_ids = ingest_documents(
        loader=DocumentLoader(
            paths=paths,
            glob=["*.txt", "*.md"],
            use_multithreading=threads > 1,
            workers=threads,
            recursive=recursive,
        ),
        splitter=RecursiveTextSplitterWithHash(
            enable_hash=True,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
        ),
        vector_store=Chroma(
            collection_name="research_docs",
            persist_directory=persist_dir,
            embedding_function=embedder,
        ),
        cache=JsonCache(),
    )
    logger.info(f"Total chunks processed: {len(doc_ids)}")
    logger.info(
        f"Total time taken to ingest: {(time.perf_counter() - start_time)} seconds"
    )

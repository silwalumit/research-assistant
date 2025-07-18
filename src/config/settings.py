from pydantic import Field

from src.config.base import BaseSettings
from src.config.db import VectorStoreSettings
from src.config.llm import LLMSettings
from src.config.loader import LoaderSettings
from src.config.logging import LogSettings


class Settings(BaseSettings):
    vector_store: VectorStoreSettings = Field(validation_alias="STORE")
    llm: LLMSettings
    log: LogSettings
    loader: LoaderSettings

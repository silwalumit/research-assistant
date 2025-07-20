from pathlib import Path
from typing import Literal

from pydantic import DirectoryPath, Field

from src.config.base import BaseSettingsModel


class VectorStoreSettings(BaseSettingsModel):
    kind: Literal["Chroma", "Faiss"] = "Chroma"
    location: DirectoryPath = Field(default_factory=lambda: Path("./data/chroma/"))
    collection_name: str = "research_docs"

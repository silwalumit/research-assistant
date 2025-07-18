from src.config.base import BaseSettingsModel


class LoaderSettings(BaseSettingsModel):
    chunk_size: int = 500
    chunk_overlap: int = 100

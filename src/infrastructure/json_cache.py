import json
import pathlib

from src.domain.interfaces import Cache


class JsonCache(Cache):
    def __init__(self, path: str = ".cache/doc_ids.json"):
        self.path = pathlib.Path(path)
        self.path.parent.mkdir(exist_ok=True, parents=True)

    def load(self) -> dict[str, str]:
        if self.path.exists():
            with self.path.open(encoding="utf-8") as f:
                return json.load(f)

        return dict()

    def save(self, id_map: dict[str, str]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(id_map, f)

from typing import Any

from app.external.mongodb import MongoRepository


class VideoGenerateRepository:
    """Persistence for video generation jobs (MongoDB)."""

    def __init__(self, collection_name: str = "video_generate") -> None:
        self._db = MongoRepository(collection_name)

    def insert_one(self, document: dict[str, Any]) -> str:
        inserted = self._db.insert_one(document)
        return str(inserted)

    def find_by_id(self, doc_id: str) -> dict[str, Any] | None:
        return self._db.find_by_id(doc_id)

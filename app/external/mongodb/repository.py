from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import DeleteOne, InsertOne, ReplaceOne, UpdateOne
from pymongo.collection import Collection
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.external.mongodb.client import get_mongodb_client


class MongoRepository:
    """CRUD-style access to a MongoDB collection via the shared client."""

    def __init__(self, collection_name: str | None = None) -> None:
        self._collection: Collection = get_mongodb_client().collection(collection_name)

    @property
    def collection(self) -> Collection:
        return self._collection

    def find_one(self, filter: Mapping[str, Any]) -> dict[str, Any] | None:
        return self._collection.find_one(dict(filter))

    def find_many(
        self,
        filter: Mapping[str, Any],
        *,
        skip: int = 0,
        limit: int = 0,
        sort: list[tuple[str, int]] | None = None,
    ) -> list[dict[str, Any]]:
        cursor = self._collection.find(
            dict(filter),
            skip=skip,
            limit=limit,
            sort=sort,
        )
        return list(cursor)

    def find_by_id(self, id: str | ObjectId) -> dict[str, Any] | None:
        try:
            oid = ObjectId(id) if isinstance(id, str) else id
        except (InvalidId, TypeError):
            return None
        return self._collection.find_one({"_id": oid})

    def insert_one(self, document: Mapping[str, Any]) -> Any:
        result: InsertOneResult = self._collection.insert_one(dict(document))
        return result.inserted_id

    def insert_many(self, documents: Sequence[Mapping[str, Any]]) -> list[Any]:
        docs = [dict(d) for d in documents]
        result = self._collection.insert_many(docs)
        return list(result.inserted_ids)

    def update_one(
        self,
        filter: Mapping[str, Any],
        update: Mapping[str, Any],
        *,
        upsert: bool = False,
    ) -> UpdateResult:
        return self._collection.update_one(dict(filter), dict(update), upsert=upsert)

    def update_by_id(
        self,
        id: str | ObjectId,
        update: Mapping[str, Any],
        *,
        upsert: bool = False,
    ) -> UpdateResult | None:
        try:
            oid = ObjectId(id) if isinstance(id, str) else id
        except (InvalidId, TypeError):
            return None
        return self._collection.update_one({"_id": oid}, dict(update), upsert=upsert)

    def replace_one(
        self,
        filter: Mapping[str, Any],
        replacement: Mapping[str, Any],
        *,
        upsert: bool = False,
    ) -> UpdateResult:
        return self._collection.replace_one(dict(filter), dict(replacement), upsert=upsert)

    def delete_one(self, filter: Mapping[str, Any]) -> int:
        result: DeleteResult = self._collection.delete_one(dict(filter))
        return int(result.deleted_count)

    def delete_many(self, filter: Mapping[str, Any]) -> int:
        result: DeleteResult = self._collection.delete_many(dict(filter))
        return int(result.deleted_count)

    def delete_by_id(self, id: str | ObjectId) -> int:
        try:
            oid = ObjectId(id) if isinstance(id, str) else id
        except (InvalidId, TypeError):
            return 0
        result: DeleteResult = self._collection.delete_one({"_id": oid})
        return int(result.deleted_count)

    def bulk_write(
        self,
        operations: list[InsertOne | UpdateOne | ReplaceOne | DeleteOne],
        *,
        ordered: bool = True,
    ) -> Any:
        return self._collection.bulk_write(operations, ordered=ordered)

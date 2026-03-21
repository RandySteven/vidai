from __future__ import annotations

import threading

from pymongo import MongoClient as PyMongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.external.config_loader import load_service_config

_mongodb_client: MongoDBClient | None = None
_mongodb_lock = threading.Lock()


class MongoDBClient:
    def __init__(
        self,
        uri: str,
        database: str,
        default_collection: str,
        *,
        server_selection_timeout_ms: int = 30_000,
        tls_allow_invalid_certificates: bool = False,
        app_name: str | None = None,
    ) -> None:
        kwargs: dict = {
            "serverSelectionTimeoutMS": server_selection_timeout_ms,
        }
        if app_name:
            kwargs["appname"] = app_name
        if tls_allow_invalid_certificates:
            kwargs["tlsAllowInvalidCertificates"] = True
        self._client: PyMongoClient = PyMongoClient(uri, **kwargs)
        self.database: Database = self._client[database]
        self.default_collection: Collection = self.database[default_collection]

    def collection(self, name: str | None = None) -> Collection:
        if name is None:
            return self.default_collection
        return self.database[name]

    def close(self) -> None:
        self._client.close()


def get_mongodb_client() -> MongoDBClient:
    global _mongodb_client
    with _mongodb_lock:
        if _mongodb_client is None:
            cfg = load_service_config()["mongodb"]
            _mongodb_client = MongoDBClient(
                uri=str(cfg["uri"]).strip(),
                database=str(cfg["database"]),
                default_collection=str(cfg["collection"]),
                server_selection_timeout_ms=int(cfg.get("server_selection_timeout_ms", 30_000)),
                tls_allow_invalid_certificates=bool(
                    cfg.get("tls_allow_invalid_certificates", False)
                ),
                app_name=cfg.get("app_name"),
            )
    return _mongodb_client


def reset_mongodb_client() -> None:
    global _mongodb_client
    with _mongodb_lock:
        if _mongodb_client is not None:
            _mongodb_client.close()
            _mongodb_client = None

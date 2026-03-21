from __future__ import annotations

import ssl
import threading
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, sessionmaker

from app.external.config_loader import load_service_config

_mysql_client: MySQLClient | None = None
_mysql_lock = threading.Lock()


class MySQLClient:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._session_local = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=Session,
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    def session_local(self) -> Session:
        return self._session_local()

    def dispose(self) -> None:
        self._engine.dispose()


def _mysql_connect_args(cfg: dict) -> dict | None:
    """TLS for Aiven / managed MySQL. Use ssl_mode=disabled for local Docker."""
    mode = str(cfg.get("ssl_mode") or "required").strip().lower()
    if mode in ("disabled", "off", "false", "0"):
        return None
    ca_path = (cfg.get("ssl_ca_path") or "").strip()
    if mode in ("verify_identity", "verify-full", "verify_full"):
        ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        if ca_path:
            ctx.load_verify_locations(ca_path)
        return {"ssl": ctx}
    if mode in ("required", "require", "true", "1"):
        ctx = ssl.create_default_context()
        if ca_path:
            ctx.load_verify_locations(ca_path)
        return {"ssl": ctx}
    ctx = ssl.create_default_context()
    if ca_path:
        ctx.load_verify_locations(ca_path)
    return {"ssl": ctx}


def get_mysql_client() -> MySQLClient:
    global _mysql_client
    with _mysql_lock:
        if _mysql_client is None:
            cfg = load_service_config()["mysql"]
            pw = cfg.get("password")
            if pw == "":
                pw = None
            url = URL.create(
                "mysql+pymysql",
                username=str(cfg["user"]),
                password=pw,
                host=str(cfg["host"]),
                port=int(cfg["port"]),
                database=str(cfg["database"]),
            )
            connect_args = _mysql_connect_args(cfg)
            engine = create_engine(
                url,
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args=connect_args or {},
            )
            _mysql_client = MySQLClient(engine)
    return _mysql_client


def reset_mysql_client() -> None:
    global _mysql_client
    with _mysql_lock:
        if _mysql_client is not None:
            _mysql_client.dispose()
            _mysql_client = None


def mysql_db_session() -> Iterator[Session]:
    """FastAPI dependency: yield a Session; commit in the service when you persist writes."""
    session = get_mysql_client().session_local()
    try:
        yield session
    finally:
        session.close()

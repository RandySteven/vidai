from __future__ import annotations

from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import CursorResult, Row
from sqlalchemy.orm import Session

from app.external.mysql.client import get_mysql_client


class MySQLRepository:
    """SQL helpers on a Session (injected per request) or short-lived sessions."""

    def __init__(self, session: Session | None = None) -> None:
        self._session = session

    @contextmanager
    def _session_scope(self):
        if self._session is not None:
            yield self._session
            return
        session = get_mysql_client().session_local()
        try:
            yield session
        finally:
            session.close()

    def fetch_one(
        self,
        sql: str,
        params: Mapping[str, Any] | None = None,
    ) -> Row[Any] | None:
        stmt = text(sql)
        with self._session_scope() as session:
            return session.execute(stmt, params or {}).first()

    def fetch_all(
        self,
        sql: str,
        params: Mapping[str, Any] | None = None,
    ) -> Sequence[Row[Any]]:
        stmt = text(sql)
        with self._session_scope() as session:
            return session.execute(stmt, params or {}).all()

    def fetch_scalars(
        self,
        sql: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[Any]:
        """Best for single-column selects; uses the first column of each row."""
        stmt = text(sql)
        with self._session_scope() as session:
            result = session.execute(stmt, params or {})
            return list(result.scalars().all())

    def execute(
        self,
        sql: str,
        params: Mapping[str, Any] | None = None,
        *,
        commit: bool = False,
    ) -> CursorResult[Any]:
        stmt = text(sql)
        if self._session is not None:
            result = self._session.execute(stmt, params or {})
            if commit:
                self._session.commit()
            return result
        with get_mysql_client().session_local() as session:
            if commit:
                with session.begin():
                    return session.execute(stmt, params or {})
            return session.execute(stmt, params or {})

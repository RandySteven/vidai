from __future__ import annotations

import json
from typing import Any

from app.external.redis.client import get_redis_client


class RedisCache:
    """String and JSON helpers on top of the shared Redis client."""

    def __init__(self, key_prefix: str = "vidai:") -> None:
        self._prefix = key_prefix
        self._redis = get_redis_client()

    def _namespaced(self, key: str) -> str:
        return f"{self._prefix}{key}"

    def get(self, key: str) -> str | None:
        return self._redis.get(self._namespaced(key))

    def get_json(self, key: str) -> Any | None:
        raw = self.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def set(self, key: str, value: str, *, ttl_seconds: int | None = None) -> None:
        name = self._namespaced(key)
        if ttl_seconds is not None:
            self._redis.set(name, value, ex=ttl_seconds)
        else:
            self._redis.set(name, value)

    def set_json(
        self,
        key: str,
        value: Any,
        *,
        ttl_seconds: int | None = None,
    ) -> None:
        self.set(key, json.dumps(value, separators=(",", ":"), default=str), ttl_seconds=ttl_seconds)

    def delete(self, *keys: str) -> int:
        if not keys:
            return 0
        names = [self._namespaced(k) for k in keys]
        return int(self._redis.delete(*names))

    def exists(self, key: str) -> bool:
        return bool(self._redis.exists(self._namespaced(key)))

    def expire(self, key: str, ttl_seconds: int) -> bool:
        return bool(self._redis.expire(self._namespaced(key), ttl_seconds))

    def incr(self, key: str, amount: int = 1) -> int:
        return int(self._redis.incrby(self._namespaced(key), amount))

    def decr(self, key: str, amount: int = 1) -> int:
        return int(self._redis.decrby(self._namespaced(key), amount))

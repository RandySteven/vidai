from __future__ import annotations

import ssl
import threading

import redis

from app.external.config_loader import load_service_config

_redis_client: redis.Redis | None = None
_redis_lock = threading.Lock()


def _build_redis_client(cfg: dict) -> redis.Redis:
    url = str(cfg.get("url") or "").strip()
    if url:
        return redis.from_url(
            url,
            decode_responses=True,
        )

    password = cfg.get("password") or None
    if password == "":
        password = None

    use_ssl = bool(cfg.get("ssl", False))
    ssl_kwargs: dict = {}
    if use_ssl:
        ssl_kwargs["ssl"] = True
        ssl_kwargs["ssl_cert_reqs"] = ssl.CERT_REQUIRED
        ca = (cfg.get("ssl_ca_path") or "").strip()
        if ca:
            ssl_kwargs["ssl_ca_certs"] = ca

    return redis.Redis(
        host=str(cfg["host"]),
        port=int(cfg["port"]),
        db=int(cfg["database"]),
        password=password,
        decode_responses=True,
        **ssl_kwargs,
    )


def get_redis_client() -> redis.Redis:
    global _redis_client
    with _redis_lock:
        if _redis_client is None:
            cfg = load_service_config()["redis"]
            _redis_client = _build_redis_client(cfg)
    return _redis_client


def reset_redis_client() -> None:
    global _redis_client
    with _redis_lock:
        if _redis_client is not None:
            _redis_client.close()
            _redis_client = None

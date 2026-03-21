from __future__ import annotations

import asyncio

from temporalio.client import Client

from app.external.config_loader import load_service_config

_temporal_client: Client | None = None
_temporal_lock = asyncio.Lock()


async def get_temporal_client() -> Client:
    global _temporal_client
    async with _temporal_lock:
        if _temporal_client is None:
            cfg = load_service_config()["temporal"]
            _temporal_client = await Client.connect(
                cfg["address"],
                namespace=cfg["namespace"],
                lazy=True,
            )
    return _temporal_client


async def reset_temporal_client() -> None:
    global _temporal_client
    async with _temporal_lock:
        _temporal_client = None

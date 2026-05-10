import asyncio
from app.external.redis.client import get_redis_client

class RedisPubSub:

    def __init__(self) -> None:
        self._redis = get_redis_client()
        self._pubsub = self._redis.pubsub()

    def pub(self, channel: str, message: str):
        self._redis.publish(channel, message)

    def sub(self, channel):
        self._pubsub.subscribe(channel)
        for message in self._pubsub.listen():
            if message['type'] == 'message':
                yield message['data'].decode()

    async def async_sub(self, channel):
        loop = asyncio.get_event_loop()
        queue: asyncio.Queue[str] = asyncio.Queue()

        def _blocking_listen():
            for data in self.sub(channel):
                loop.call_soon_threadsafe(queue.put_nowait, data)

        loop.run_in_executor(None, _blocking_listen)

        while True:
            yield await queue.get()
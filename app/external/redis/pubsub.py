from app.external.redis.client import get_redis_client

class RedisPubSub:

    def __init__(self) -> None:
        self._redis = get_redis_client()
        self._pubsub = self._redis.pubsub()

    def pub(self, channel: str, message: str):
        self._redis.publish(channel, message)

    def sub(self, channel):
        self._pubsub.subscribe(channel)

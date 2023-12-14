import json

import aioredis

from server.models.chat_message import ChatMessage
from settings import get_settings

settings = get_settings()


class RedisPubSubManager:

    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT):
        self.redis_connection = None
        self.redis_host = host
        self.redis_port = port
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        return aioredis.Redis(host=self.redis_host, port=self.redis_port)

    async def connect(self) -> None:
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, room_id: str, message: ChatMessage) -> None:
        serialized_message = json.dumps(message.to_dict())
        if not self.redis_connection:
            self.redis_connection = await self._get_redis_connection()
        print(self.redis_connection, 'redis connection')
        await self.redis_connection.publish(room_id, serialized_message)

    async def subscribe(self, room_id: str) -> aioredis.Redis:

        await self.pubsub.subscribe(room_id)
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        await self.pubsub.unsubscribe(room_id)
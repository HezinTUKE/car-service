from __future__ import annotations

import json
from asyncio import Lock

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractMessage, AbstractChannel, AbstractRobustConnection, AbstractExchange

from application import config
from application.enums.services.rabbit_routers import ListenRabbitRouter, PublishRabbitRouter

mb_config = config.rabbitmq

_instance: RabbitProcessor | None = None
_lock = Lock()


async def get_rabbit_processor():
    global _instance
    async with _lock:
        if _instance is None:
            connection = await connect_robust(
                f"amqp://{mb_config.username}:{mb_config.password}@{mb_config.host}:{mb_config.port}/"
            )
            channel: AbstractChannel = await connection.channel()
            await channel.set_qos(prefetch_count=10)
            exchange = await channel.declare_exchange(mb_config.exchange, "topic", durable=mb_config.durable)
            _instance = RabbitProcessor(connection, channel, exchange)
    return _instance


async def close_rabbit_processor():
    global _instance
    async with _lock:
        if _instance:
            await _instance.disconnect()
            _instance = None


class RabbitProcessor:
    def __init__(self, connection: AbstractRobustConnection, channel: AbstractChannel, exchange: AbstractExchange):
        self.connection = connection
        self.channel = channel
        self.exchange = exchange

    async def listen(self):
        exchange = await self.channel.declare_exchange(mb_config.exchange, "topic", durable=mb_config.durable)
        queue = await self.channel.declare_queue(mb_config.queue, durable=mb_config.durable)

        for router in ListenRabbitRouter:
            await queue.bind(exchange, routing_key=f"*.{router.value}")

        await queue.consume(self.process_message)

    async def process_message(self, message: AbstractMessage):
        pass

    async def publish(self, routing_key: PublishRabbitRouter, message: dict):
        str_message = json.dumps(message).encode()
        await self.exchange.publish(Message(body=str_message), routing_key=f"{config.origin}.{routing_key.value}")

    async def disconnect(self):
        await self.channel.close()
        await self.connection.close()

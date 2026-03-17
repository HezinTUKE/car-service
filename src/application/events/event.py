from __future__ import annotations

import os
import json
from asyncio import Lock
from dotenv import load_dotenv
from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractMessage, AbstractChannel, AbstractRobustConnection, AbstractExchange

from application.enums.services.rabbit_routers import ListenRabbitRouter, PublishRabbitRouter

load_dotenv()


_instance: RabbitProcessor | None = None
_lock = Lock()


async def get_rabbit_processor():
    global _instance

    username = os.getenv("AMQP_USERNAME")
    password = os.getenv("AMQP_PASSWORD")
    host = os.getenv("AMQP_HOST", "localhost")
    port = int(os.getenv("AMQP_PORT", 5672))
    exchange = os.getenv("AMQP_EXCHANGE")
    durable = os.getenv("AMQP_DURABLE", True)

    async with _lock:
        if _instance is None:
            url = f"amqp://{username}:{password}@{host}:{port}/"
            connection = await connect_robust(url)
            channel: AbstractChannel = await connection.channel()
            await channel.set_qos(prefetch_count=10)
            exchange = await channel.declare_exchange(exchange, "topic", durable=durable)
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

        self.origin = os.getenv("ORIGIN", "CarService")
        self.queue = os.getenv("AMQP_QUEUE", "events_queue")
        self.durable = os.getenv("AMQP_DURABLE", True)

    async def listen(self):
        exchange = await self.channel.declare_exchange(self.exchange, "topic", durable=self.durable)
        queue = await self.channel.declare_queue(self.queue, durable=self.durable)

        for router in ListenRabbitRouter:
            await queue.bind(exchange, routing_key=f"*.{router.value}")

        await queue.consume(self.process_message)

    async def process_message(self, message: AbstractMessage):
        pass

    async def publish(self, routing_key: PublishRabbitRouter, message: dict):
        str_message = json.dumps(message).encode()
        await self.exchange.publish(Message(body=str_message), routing_key=f"{self.origin}.{routing_key.value}")

    async def disconnect(self):
        await self.channel.close()
        await self.connection.close()

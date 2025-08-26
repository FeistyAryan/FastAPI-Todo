import asyncio
import aio_pika
import json
import structlog
from contextlib import asynccontextmanager

log = structlog.get_logger()

class RabbitMQManager:
    def __init__(self, host="rabbitmq"):
        self.host = host
        self._connection = None
        self._channel = None
        self._connection_lock = asyncio.Lock()

    async def _get_connection(self):
        if self._connection is None or self._connection.is_closed:
            async with self._connection_lock:
                # Double-check inside the lock to prevent race conditions
                if self._connection is None or self._connection.is_closed:
                    log.info("Attempting to connect to RabbitMQ...")
                    try:
                        self._connection = await aio_pika.connect_robust(host=self.host)
                        self._connection.close_callbacks.add(self._handle_connection_close)
                        log.info("Successfully connected to RabbitMQ")
                    except:
                        log.error("Failed to connect to RabbitMQ")
                        raise
        return self._connection

    def _handle_connection_close(self):
        log.warn("RabbitMQ connection closed. It will be re-established on next use.", exc_info=exc)
        self._connection = None

    async def get_channel(self):
        if self._channel is None or self._channel.is_closed:
            connection = await self._get_connection()
            self._channel = await connection.channel()
        return self._channel

    async def publish_message(self, queue_name, message_body: dict):
        try:
            channel = await self.get_channel()
            queue = await channel.declare_queue(queue_name, durable=True)
            await channel.default.exchange_publish(
                aio_pika.Message(
                    body=json.dumps(message_body).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue.name,
            )
            log.info("Message published successfully", queue=queue_name)
        except Exception as e:
            log.error("Failed to publish message", error=str(e), queue=queue_name)

    async def close(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        log.info("RabbitMQ connection closed.")

rabbitmq_manager = RabbitMQManager()
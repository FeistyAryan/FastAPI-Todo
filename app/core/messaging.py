import aio_pika
import json
import structlog

log = structlog.get_logger()

async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(host="rabbitmq")

async def publish_message(queue_name: str, message_body: dict):
    try:
        connection = await get_rabbitmq_connection()
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message_body).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue.name,
            )
        log.info("Message published successfully", queue=queue_name, message=message_body)
    except Exception as e:
        log.error("Failed to publish message", error=str(e), queue=queue_name)

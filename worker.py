import asyncio
import aio_pika
import json
import structlog
from app.core.context import request_id_var

log = structlog.get_logger()

async def on_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        body = message.body.decode()
        try:
            data = json.loads(body)
            request_id = data.get("request_id", "N/A")
            email = data.get("email")
            log.info(
                    "Received password reset request",
                    email=email,
                    request_id=request_id
            )
            await asyncio.sleep(2) # Simulate sending email
            log.info(
                "Password reset email sent (simulated)",
                email=email,
                request_id=request_id
            )
        except json.JSONDecodeError:
            log.error("Failed to decode message body", body=body)


async def main():
    while True:
        try:
            connection = await aio_pika.connect_robust(host='rabbitmq')
            break
        except ConnectionError:
            log.info("RabbitMQ not ready yet, waiting...", request_id=str(request_id_var.get()))
            await asyncio.sleep(5)
    
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue("password_reset_queue", durable=True)
        log.info("Worker is waiting for messages...")
        await queue.consume(on_message)
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
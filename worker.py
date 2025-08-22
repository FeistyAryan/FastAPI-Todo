import asyncio
import json
import structlog

from app.core.rabbitmq import rabbitmq_manager
from app.core.context import request_id_var
from aio_pika.abc import AbstractIncomingMessage

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
    channel = await rabbitmq_manager.get_channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue("password_reset_queue", durable=True)
    
    log.info("Worker is waiting for messages...")
    await queue.consume(on_message)
    try:
        await asyncio.Future()
    finally:
        await rabbitmq_manager.close()

if __name__ == '__main__':
    asyncio.run(main())
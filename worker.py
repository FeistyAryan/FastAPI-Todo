import asyncio
import json
import structlog
from aio_pika.abc import AbstractIncomingMessage

from app.models.user import User
from app.models.session import Session
from app.models.password_reset_token import PasswordResetToken

from app.core.rabbitmq import rabbitmq_manager
from app.core.context import request_id_var
from app.db import get_db
from app.services.user_service import user_service
from app.services.email_service import email_service

log = structlog.get_logger()

async def on_message(message: AbstractIncomingMessage):
    async with message.process():
        body = message.body.decode()
        try:
            data = json.loads(body)
            request_id = data.get("request_id", "N/A")
            email = data.get("email")
            request_id_var.set(request_id)  #set contextvar for logging as worker is operating from a different container
            log.info(
                    "Received password reset request",
                    email=email,
                    request_id=request_id
            )
            async for db in get_db():
                result = await user_service.process_password_reset(db=db, email=email)

                if result:
                    email_to, raw_token = result
                    await email_service.send_password_reset_email(email_to=email_to, reset_token=raw_token)
                    log.info("Password reset email sent", email=email_to, request_id=request_id)

        except json.JSONDecodeError:
            log.error("Failed to decode message body", body=body)
        except Exception as e:
            log.exception("Unhandled error in worker", exc_info=e)


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
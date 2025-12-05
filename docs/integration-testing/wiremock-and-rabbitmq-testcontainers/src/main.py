import os
import asyncio
import logging
import requests

from aio_pika import connect_robust


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    connection = await connect_robust(
        os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    )

    async with connection:
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        exchange = await channel.declare_exchange(
            name="test_exchange",
            type="direct",
            durable=True,
            passive=True if os.getenv("ENV", "") == "prod" else False,
        )
        queue = await channel.declare_queue(name="test_queue", durable=True)

        await queue.bind(
            exchange=exchange,
            routing_key="test_routing_key",
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    decoded_message = message.body.decode()
                    requests.post(
                        decoded_message["callbackUrl"],
                        data={"message": f"Hi {decoded_message['name']}!"},
                        timeout=5,
                    )


if __name__ == "__main__":
    asyncio.run(main())

import pika
import constants
from time import sleep
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import random


# Create connection string
connection_params = pika.ConnectionParameters("localhost", 5672)
# Create connection
connection = pika.BlockingConnection(connection_params)
# Create a channel
channel = connection.channel()
# Declare queue
channel.queue_declare(constants.REGISTERED_USER_QUEUE)
# No round robin distribution strategy
channel.basic_qos(prefetch_count=1)


def handle_message(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    message: bytes,
) -> None:
    """Handle messages"""
    processing_time = random.randint(1, 10)
    sleep(processing_time)
    print(f"Message: {str(message)}, processed in: {processing_time}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Consume messages
channel.basic_consume(constants.REGISTERED_USER_QUEUE, handle_message, False)
channel.start_consuming()

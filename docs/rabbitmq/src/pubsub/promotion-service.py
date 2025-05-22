import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties
import constants


# Create connection string
connection_params = pika.ConnectionParameters("localhost", 5672)
# Create connection
connection = pika.BlockingConnection(connection_params)
# Create a channel
channel = connection.channel()
# Declare a fanout exchange
channel.exchange_declare(constants.PUBSUB_EXCHANGE, ExchangeType.fanout)
# Declare a temporary queue
queue = channel.queue_declare('', exclusive=True)
queue_name = queue.method.queue
# Bind the queue to fanout exchange
channel.queue_bind(queue_name, constants.PUBSUB_EXCHANGE)


def handle_message(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    message: bytes,
) -> None:
    """Handle message"""

    print(f"Promotion service received {str(message)}")


# Consume messages
channel.basic_consume(queue_name,
                      handle_message,
                      True)
channel.start_consuming()

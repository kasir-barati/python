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
# Declare a direct exchange
channel.exchange_declare(constants.DIRECT_EXCHANGE, ExchangeType.direct)
# Declare analytics queue
channel.queue_declare(constants.ANALYTICS_QUEUE_NAME)
# Bind the queue to the channel
channel.queue_bind(constants.ANALYTICS_QUEUE_NAME,
                   constants.DIRECT_EXCHANGE,
                   constants.ANALYTICS_ROUTING_KEY)


def handle_message(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    message: bytes,
) -> None:
    """Handle messages"""
    print(f"Analytics service: {str(message)}")


# Consume messages
channel.basic_consume(
    constants.ANALYTICS_QUEUE_NAME,
    handle_message,
    True,
)
channel.start_consuming()

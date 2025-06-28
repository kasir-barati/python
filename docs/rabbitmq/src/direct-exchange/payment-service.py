import pika
from pika.exchange_type import ExchangeType
import constants


# Create connection string
connection_params = pika.ConnectionParameters("localhost", 5672)
# Create connection
connection = pika.BlockingConnection(connection_params)
# Create a channel
channel = connection.channel()
# Declare a direct exchange
channel.exchange_declare(constants.DIRECT_EXCHANGE, ExchangeType.direct)
# Declare queue
channel.queue_declare(constants.PAYMENT_CREATED_QUEUE_NAME)
# Bind the queue
channel.queue_bind(constants.PAYMENT_CREATED_QUEUE_NAME,
                   constants.DIRECT_EXCHANGE, constants.ANALYTICS_ROUTING_KEY)


# Consume messages
channel.basic_consume(
    constants.REGISTERED_USER_QUEUE,
    lambda ch, method, properties, message: print(message),
    True,
)
channel.start_consuming()

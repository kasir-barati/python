import pika
from pika.exchange_type import ExchangeType
from payload_interfaces import RegisteredUserPayload
import constants

# The connection string
connection_params = pika.ConnectionParameters("localhost", 5672)
# Create connection
connection = pika.BlockingConnection(connection_params)
# Create a channel
channel = connection.channel()
# Declare a fanout exchange
channel.exchange_declare(constants.PUBSUB_EXCHANGE, ExchangeType.fanout)


# Broadcast a message
message: RegisteredUserPayload = {
    "id": "682b603add4c8a3287bb54c0",
    "name": "Mohammad Jawad",
}
channel.basic_publish(constants.PUBSUB_EXCHANGE, "", str(message))

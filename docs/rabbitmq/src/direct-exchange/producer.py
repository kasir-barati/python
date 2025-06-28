import pika
from pika.exchange_type import ExchangeType
from payload_interfaces import UserCreatedPayload
import constants

# The connection string
connection_params = pika.ConnectionParameters("localhost", 5672)
# Create connection
connection = pika.BlockingConnection(connection_params)
# Create a channel
channel = connection.channel()
# Declare a direct exchange
channel.exchange_declare(constants.DIRECT_EXCHANGE, ExchangeType.direct)

# Produce a message
message: UserCreatedPayload = {
    "id": "682b603add4c8a3287bb54c0",
    "name": "Mohammad Jawad",
}
channel.basic_publish(constants.DIRECT_EXCHANGE,
                      constants.ANALYTICS_ROUTING_KEY,
                      str(message))

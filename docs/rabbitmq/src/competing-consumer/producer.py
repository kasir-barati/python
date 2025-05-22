import random
from time import sleep
import uuid
import pika
from payload_interfaces import RegisteredUserPayload
import constants

# The connection string
connection_params = pika.ConnectionParameters("localhost", 5672)
# Create connection
connection = pika.BlockingConnection(connection_params)
# Create a channel
channel = connection.channel()
# Declare a queue
channel.queue_declare(constants.REGISTERED_USER_QUEUE)


while True:
    # Produce a message
    message: RegisteredUserPayload = {
        "id": str(uuid.uuid4()),
        "name": "Mohammad Jawad",
    }
    channel.basic_publish("", constants.REGISTERED_USER_QUEUE_ROUTING_KEY, str(message))
    sleep(random.randint(1, 3))

import pika
import constants


# Create connection string
connection_params = pika.ConnectionParameters("localhost", 5672)
# Create connection
connection = pika.BlockingConnection(connection_params)
# Create a channel
channel = connection.channel()
# Declare queue
channel.queue_declare(constants.REGISTERED_USER_QUEUE)


# Consume messages
channel.basic_consume(
    constants.REGISTERED_USER_QUEUE,
    lambda ch, method, properties, message: print(message),
    True,
)
channel.start_consuming()

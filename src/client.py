from typing import cast

from grpc import insecure_channel

from greet_pb2 import GreetMeRequest, GreetMeResponse
from greet_pb2_grpc import GreetServiceStub

channel = insecure_channel("localhost:50051")

client = GreetServiceStub(channel)
# It's called a stub because the client itself doesn't have any functionality. It calls out to a remote server and passes the result back.
# The protobuf compiler takes this microservice name, GreetService, and appends Stub to it to form the client name, GreetServiceStub.

response = cast(
    GreetMeResponse,
    client.GreetMe(
        GreetMeRequest(name="Mohammad Jawad", language="de")
    ),
)

print(response)

# client.SubscribeToNotifications()

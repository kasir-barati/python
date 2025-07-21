from typing import cast

from grpc import insecure_channel

from .stubs.greet_pb2 import (
    SubscribeToNotificationsRequest,
    SubscribeToNotificationsResponse,
)
from .stubs.greet_pb2_grpc import GreetServiceStub

with insecure_channel("localhost:50051") as channel:
    client = GreetServiceStub(channel)
    # It's called a stub because the client itself doesn't have any functionality. It calls out to a remote server and passes the result back.
    # The protobuf compiler takes this microservice name, GreetService, and appends Stub to it to form the client name, GreetServiceStub.

    request = SubscribeToNotificationsRequest()
    request.notification_type = "error"
    responses = cast(
        list[SubscribeToNotificationsResponse],
        client.SubscribeToNotifications(request),
    )

    for response in responses:
        print(response)

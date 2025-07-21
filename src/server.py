from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

from grpc import StatusCode, server

from .stubs.greet_pb2 import (
    SubscribeToNotificationsRequest,
    SubscribeToNotificationsResponse,
)
from .stubs.greet_pb2_grpc import (
    GreetService,
    add_GreetServiceServicer_to_server,
)


class GreetServiceImplementation(GreetService):
    def SubscribeToNotifications(
        self, request: SubscribeToNotificationsRequest, context: Any
    ):
        metadata = dict(context.invocation_metadata())

        print(metadata)

        if request.notification_type.strip() == "":
            context.abort(
                StatusCode.INVALID_ARGUMENT, "name should be provided"
            )
            return

        for index in range(10):
            response = SubscribeToNotificationsResponse()
            response.content = "something went wrong"
            response.title = "Error #123"
            response.type = "error"
            response.is_blocking = True

            yield response
            sleep(5)


if __name__ == "__main__":
    my_server = server(ThreadPoolExecutor(max_workers=10))
    add_GreetServiceServicer_to_server(
        GreetServiceImplementation(), my_server
    )
    my_server.add_insecure_port("[::]:50051")
    my_server.start()
    print("app is listening on [::]:50051")
    my_server.wait_for_termination()

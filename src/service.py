from concurrent.futures import ThreadPoolExecutor

from grpc import StatusCode, server

from greet_pb2 import GreetMeRequest, GreetMeResponse
from greet_pb2_grpc import (
    GreetService,
    add_GreetServiceServicer_to_server,
)


class GreetServiceImplementation(GreetService):
    def GreetMe(
        self, request: GreetMeRequest, context
    ) -> GreetMeResponse | None:
        metadata = dict(context.invocation_metadata())
        print(metadata)

        if request.name.strip() == "":
            context.abort(
                StatusCode.INVALID_ARGUMENT, "name should be provided"
            )
            return
        if request.language.strip() == "":
            context.abort(
                StatusCode.INVALID_ARGUMENT,
                "language should be provided",
            )
            return

        return GreetMeResponse(
            f"Hallo {request.name}"
            if request.language == "de"
            else f"Hi {request.name}"
        )


if __name__ == "__main__":
    my_server = server(ThreadPoolExecutor(max_workers=10))
    add_GreetServiceServicer_to_server(
        GreetServiceImplementation(), my_server
    )
    my_server.add_insecure_port("[::]:50051")
    my_server.start()
    print("app is listening on [::]:50051")
    my_server.wait_for_termination()

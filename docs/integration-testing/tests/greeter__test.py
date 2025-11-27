import pytest
import grpc
from concurrent import futures

from stubs.helloworld_pb2 import HelloReply, HelloRequest
from stubs.helloworld_pb2_grpc import (
    GreeterServicer,
    add_GreeterServicer_to_server,
    GreeterStub,
)


class MockGreeter(GreeterServicer):
    def SayHello(self, request, context):
        return HelloReply(message=f"Hello, {request.name}!")


@pytest.fixture(scope="module")
def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_GreeterServicer_to_server(MockGreeter(), server)
    port = server.add_insecure_port("[::]:0")
    server.start()
    yield f"localhost:{port}"
    server.stop(None)


def test_grpc_client(grpc_server):
    channel = grpc.insecure_channel(grpc_server)
    stub = GreeterStub(channel)
    response = stub.SayHello(HelloRequest(name="pytest"))
    assert response.message == "Hello, pytest!"

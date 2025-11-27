import grpc

from stubs.helloworld_pb2 import HelloRequest
from stubs.helloworld_pb2_grpc import GreeterStub


def test_grpc_client(grpc_server):
    print(f"🧪 TEST 1: Using server at {grpc_server}")
    channel = grpc.insecure_channel(grpc_server)
    stub = GreeterStub(channel)

    response = stub.SayHello(HelloRequest(name="pytest"))

    assert response.message == "Hello, pytest!"


def test_grpc_client_second_call(grpc_server):
    print(f"🧪 TEST 2: Using server at {grpc_server}")
    channel = grpc.insecure_channel(grpc_server)
    stub = GreeterStub(channel)

    response = stub.SayHello(HelloRequest(name="second-test"))

    assert response.message == "Hello, second-test!"

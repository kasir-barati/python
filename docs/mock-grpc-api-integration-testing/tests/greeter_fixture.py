import pytest
import grpc
from concurrent import futures

from stubs.helloworld_pb2 import HelloReply
from stubs.helloworld_pb2_grpc import add_GreeterServicer_to_server, GreeterServicer


class MockGreeter(GreeterServicer):
    def SayHello(self, request, context):
        return HelloReply(message=f"Hello, {request.name}!")


@pytest.fixture(scope="module")
def grpc_server():
    print("🚀 FIXTURE SETUP: Starting gRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_GreeterServicer_to_server(MockGreeter(), server)
    port = server.add_insecure_port("[::]:0")
    server.start()
    print(f"✅ FIXTURE SETUP: gRPC server started on port {port}")
    yield f"localhost:{port}"
    print("🧹 FIXTURE TEARDOWN: Stopping gRPC server...")
    server.stop(None)
    print("✅ FIXTURE TEARDOWN: gRPC server stopped")

import pytest
import grpc
from concurrent import futures

from stubs.helloworld_pb2 import HelloReply, UploadReply
from stubs.helloworld_pb2_grpc import add_GreeterServicer_to_server, GreeterServicer


class MockGreeter(GreeterServicer):
    def SayHello(self, request, context):
        return HelloReply(message=f"Hello, {request.name}!")

    def Upload(self, request_iterator, context):
        file_path = "/tmp/temp.txt"

        with open(file_path, "wb") as f:
            chunk_count = 0
            total_bytes = 0

            for request in request_iterator:
                if request.chunk_number == 0:
                    yield UploadReply(status="Upload completed successfully")
                    break

                # Write the data chunk to file
                f.write(request.data)
                chunk_count += 1
                total_bytes += len(request.data)

                # Yield progress response
                yield UploadReply(
                    status=f"Received chunk {request.chunk_number}, {len(request.data)} bytes"
                )

        print(
            f"📁 Upload complete: {total_bytes} bytes written to {file_path} in {chunk_count} chunks"
        )


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

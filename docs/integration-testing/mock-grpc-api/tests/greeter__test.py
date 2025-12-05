import grpc
import os
from pytest import MonkeyPatch
from stubs.helloworld_pb2 import HelloRequest
from stubs.helloworld_pb2_grpc import GreeterStub
from main import main


def test_grpc_client(grpc_server):
    channel = grpc.insecure_channel(grpc_server)
    stub = GreeterStub(channel)

    response = stub.SayHello(HelloRequest(name="pytest"))

    assert response.message == "Hello, pytest!"


def test_grpc_client_second_call(grpc_server):
    channel = grpc.insecure_channel(grpc_server)
    stub = GreeterStub(channel)

    response = stub.SayHello(HelloRequest(name="second-test"))

    assert response.message == "Hello, second-test!"


def test_should_upload_text(grpc_server, monkeypatch: MonkeyPatch):
    uploaded_file_path = "/tmp/temp.txt"
    monkeypatch.setenv("FILE_SERVER_URI", grpc_server)

    main()

    assert os.path.exists(uploaded_file_path), "Upload should create a temporary file"

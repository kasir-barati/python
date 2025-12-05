from stubs.helloworld_pb2_grpc import GreeterStub
from utils.split_text_into_chunks import split_text_into_chunks
from .create_upload_request import create_upload_requests


def upload_data(stub: GreeterStub, text: str, chunk_count: int = 2):
    print(f"Uploading text in {chunk_count} chunks...")
    print(f"Original text length: {len(text)} characters")

    chunks = split_text_into_chunks(text, chunk_count)

    upload_requests = create_upload_requests(chunks)

    responses = stub.Upload(iter(upload_requests))

    for response in responses:
        print(f"Upload response: {response.status}")

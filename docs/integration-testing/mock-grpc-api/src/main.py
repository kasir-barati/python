from os import getenv
import grpc
from stubs.helloworld_pb2_grpc import GreeterStub
from upload_service.upload_data import upload_data
from utils.random_sentences import random_sentences


def main():
    with grpc.insecure_channel(getenv("FILE_SERVER_URI")) as channel:
        stub = GreeterStub(channel)
        txt = random_sentences(120)
        upload_data(stub, txt, chunk_count=2)


if __name__ == "__main__":
    main()

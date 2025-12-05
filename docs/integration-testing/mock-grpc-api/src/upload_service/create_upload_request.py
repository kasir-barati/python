from stubs.helloworld_pb2 import UploadRequest


def create_upload_requests(chunks: list[bytes]) -> list[UploadRequest]:
    requests = []

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {len(chunk)} bytes")

        request = UploadRequest()
        request.chunk_number = i + 1
        request.data = chunk

        requests.append(request)

    # Add final request with chunk_number = 0 to indicate end of upload
    end_request = UploadRequest()
    end_request.chunk_number = 0
    end_request.data = b""

    requests.append(end_request)

    return requests

def split_text_into_chunks(text: str, chunk_count: int = 2) -> list[bytes]:
    """Split text into specified number of chunks."""
    text_bytes = text.encode("utf-8")
    chunk_size = len(text_bytes) // chunk_count
    chunks = []

    for i in range(chunk_count):
        start = i * chunk_size
        # For the last chunk, include any remaining bytes
        end = start + chunk_size if i < chunk_count - 1 else len(text_bytes)
        chunks.append(text_bytes[start:end])

    return chunks

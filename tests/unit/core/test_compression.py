from minigit.core.compression import compress_bytes, decompress_bytes


def test_compress_decompress_roundtrip() -> None:
    original = b"hello world" * 100
    compressed = compress_bytes(original)
    decompressed = decompress_bytes(compressed)
    assert decompressed == original


def test_compress_reduces_size() -> None:
    original = b"a" * 1000
    compressed = compress_bytes(original)
    assert len(compressed) < len(original)
"""
Compression utilities using zlib (same as Git).
"""

import zlib


def compress_bytes(data: bytes) -> bytes:
    """Mengompres raw object bytes sebelum disimpan ke disk."""
    return zlib.compress(data)


def decompress_bytes(data: bytes) -> bytes:
    """Mendekompres bytes yang dibaca dari file objek."""
    return zlib.decompress(data)
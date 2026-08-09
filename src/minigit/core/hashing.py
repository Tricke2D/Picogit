"""
Core hashing utilities for Git objects.
Git computes hash from "header + content", not just raw content.
"""

import hashlib


def compute_object_hash(object_type: str, content: bytes) -> str:
    """
    Menghitung SHA-1 hash dari sebuah Git object.

    Args:
        object_type: "blob" | "tree" | "commit"
        content: raw bytes dari isi objek

    Returns:
        40-karakter hex string SHA-1 hash
    """
    header = f"{object_type} {len(content)}\0".encode("utf-8")
    store_bytes = header + content
    return hashlib.sha1(store_bytes).hexdigest()


def build_storable_content(object_type: str, content: bytes) -> bytes:
    """
    Menggabungkan header + content menjadi satu bytes utuh.
    """
    header = f"{object_type} {len(content)}\0".encode("utf-8")
    return header + content
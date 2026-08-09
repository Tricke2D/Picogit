from minigit.core.hashing import compute_object_hash, build_storable_content


def test_same_content_produces_same_hash() -> None:
    content = b"hello world"
    hash_a = compute_object_hash("blob", content)
    hash_b = compute_object_hash("blob", content)
    assert hash_a == hash_b


def test_different_type_produces_different_hash() -> None:
    content = b"hello world"
    blob_hash = compute_object_hash("blob", content)
    tree_hash = compute_object_hash("tree", content)
    assert blob_hash != tree_hash


def test_build_storable_content_includes_header() -> None:
    content = b"hello"
    storable = build_storable_content("blob", content)
    assert b"blob 5\0" in storable
    assert b"hello" in storable


def test_hash_is_40_characters() -> None:
    content = b"test"
    hash_val = compute_object_hash("blob", content)
    assert len(hash_val) == 40
    assert all(c in "0123456789abcdef" for c in hash_val)
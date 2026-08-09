from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit


def test_commit_serialization_roundtrip(tmp_path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")

    original = Commit.create(
        tree_hash="abc123", parent_hash=None,
        author="developer", message="initial commit",
    )
    original_hash = original.save(store)

    loaded = Commit.load(store, original_hash)
    assert loaded.tree_hash == original.tree_hash
    assert loaded.parent_hash == original.parent_hash
    assert loaded.author == original.author
    assert loaded.message == original.message


def test_second_commit_references_first_as_parent(tmp_path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")

    first = Commit.create(
        tree_hash="abc123", parent_hash=None,
        author="dev", message="first",
    )
    first_hash = first.save(store)

    second = Commit.create(
        tree_hash="def456", parent_hash=first_hash,
        author="dev", message="second",
    )
    second_hash = second.save(store)

    loaded_second = Commit.load(store, second_hash)
    assert loaded_second.parent_hash == first_hash
from pathlib import Path

from minigit.core.gc import run_garbage_collection
from minigit.core.object_store import ObjectStore
from minigit.core.objects.blob import Blob
from minigit.core.objects.commit import Commit
from minigit.core.objects.tree import Tree, TreeEntry
from minigit.core.repository import Repository


def test_gc_deletes_unreachable_commit(tmp_path: Path) -> None:
    repo = Repository(working_dir=tmp_path)
    repo.initialize()
    store = ObjectStore(objects_dir=repo.objects_dir)

    blob_hash = Blob(content=b"hello").save(store)
    tree = Tree(entries=[TreeEntry(mode="100644", obj_type="blob", obj_hash=blob_hash, name="a.txt")])
    tree_hash = tree.save(store)

    reachable_commit = Commit.create(tree_hash=tree_hash, parent_hashes=[], author="dev", message="kept")
    reachable_hash = reachable_commit.save(store)
    repo.update_branch_ref("main", reachable_hash)

    orphan_commit = Commit.create(tree_hash=tree_hash, parent_hashes=[], author="dev", message="orphan")
    orphan_hash = orphan_commit.save(store)

    deleted = run_garbage_collection(repo, store)

    assert deleted == 1
    assert not (repo.objects_dir / orphan_hash[:2] / orphan_hash[2:]).exists()
    assert (repo.objects_dir / reachable_hash[:2] / reachable_hash[2:]).exists()


def test_gc_keeps_all_reachable_objects(tmp_path: Path) -> None:
    repo = Repository(working_dir=tmp_path)
    repo.initialize()
    store = ObjectStore(objects_dir=repo.objects_dir)

    blob_hash = Blob(content=b"hello").save(store)
    tree = Tree(entries=[TreeEntry(mode="100644", obj_type="blob", obj_hash=blob_hash, name="a.txt")])
    tree_hash = tree.save(store)

    commit = Commit.create(tree_hash=tree_hash, parent_hashes=[], author="dev", message="kept")
    commit_hash = commit.save(store)
    repo.update_branch_ref("main", commit_hash)

    deleted = run_garbage_collection(repo, store)

    assert deleted == 0
    assert (repo.objects_dir / blob_hash[:2] / blob_hash[2:]).exists()
    assert (repo.objects_dir / tree_hash[:2] / tree_hash[2:]).exists()
    assert (repo.objects_dir / commit_hash[:2] / commit_hash[2:]).exists()
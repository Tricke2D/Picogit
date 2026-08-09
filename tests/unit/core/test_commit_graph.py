from minigit.core.commit_graph import find_common_ancestor
from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit


def test_finds_shared_root_as_common_ancestor(tmp_path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")

    root = Commit.create(tree_hash="t0", parent_hashes=[], author="dev", message="root")
    root_hash = root.save(store)

    branch_a = Commit.create(tree_hash="t1", parent_hashes=[root_hash], author="dev", message="a")
    branch_a_hash = branch_a.save(store)

    branch_b = Commit.create(tree_hash="t2", parent_hashes=[root_hash], author="dev", message="b")
    branch_b_hash = branch_b.save(store)

    ancestor = find_common_ancestor(store, branch_a_hash, branch_b_hash)
    assert ancestor == root_hash


def test_finds_ancestor_with_deeper_graph(tmp_path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")

    root = Commit.create(tree_hash="t0", parent_hashes=[], author="dev", message="root")
    root_hash = root.save(store)

    commit1 = Commit.create(tree_hash="t1", parent_hashes=[root_hash], author="dev", message="c1")
    commit1_hash = commit1.save(store)

    commit2 = Commit.create(tree_hash="t2", parent_hashes=[commit1_hash], author="dev", message="c2")
    commit2_hash = commit2.save(store)

    commit3 = Commit.create(tree_hash="t3", parent_hashes=[commit2_hash], author="dev", message="c3")
    commit3_hash = commit3.save(store)

    ancestor = find_common_ancestor(store, commit3_hash, commit2_hash)
    assert ancestor == commit2_hash
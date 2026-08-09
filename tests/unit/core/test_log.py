from minigit.core.log import walk_commit_log
from minigit.core.object_store import ObjectStore
from minigit.core.objects.commit import Commit


def test_log_does_not_duplicate_commit_reached_via_two_parents(tmp_path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")

    root = Commit.create(tree_hash="t0", parent_hashes=[], author="dev", message="root")
    root_hash = root.save(store)

    branch_a = Commit.create(tree_hash="t1", parent_hashes=[root_hash], author="dev", message="a")
    branch_a_hash = branch_a.save(store)

    branch_b = Commit.create(tree_hash="t2", parent_hashes=[root_hash], author="dev", message="b")
    branch_b_hash = branch_b.save(store)

    merge = Commit.create(
        tree_hash="t3", parent_hashes=[branch_a_hash, branch_b_hash],
        author="dev", message="merge",
    )
    merge_hash = merge.save(store)

    entries = walk_commit_log(store, merge_hash)
    hashes = [h for h, _ in entries]

    assert hashes.count(root_hash) == 1
    assert len(hashes) == 4  # merge, a, b, root


def test_log_shows_commits_in_order(tmp_path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")

    root = Commit.create(tree_hash="t0", parent_hashes=[], author="dev", message="root")
    root_hash = root.save(store)

    c1 = Commit.create(tree_hash="t1", parent_hashes=[root_hash], author="dev", message="first")
    c1_hash = c1.save(store)

    c2 = Commit.create(tree_hash="t2", parent_hashes=[c1_hash], author="dev", message="second")
    c2_hash = c2.save(store)

    entries = walk_commit_log(store, c2_hash)
    hashes = [h for h, _ in entries]

    assert hashes[0] == c2_hash
    assert hashes[1] == c1_hash
    assert hashes[2] == root_hash
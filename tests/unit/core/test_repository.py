from pathlib import Path

from minigit.core.repository import Repository


def test_new_branch_points_to_same_commit_as_source(tmp_path: Path) -> None:
    repo = Repository(working_dir=tmp_path)
    repo.initialize()
    repo.update_branch_ref("main", "fake_commit_hash_abc")

    repo.create_branch("feature")

    assert repo.get_branch_commit_hash("feature") == "fake_commit_hash_abc"
    assert "feature" in repo.list_branches()
    assert "main" in repo.list_branches()


def test_list_branches_returns_empty_for_new_repo(tmp_path: Path) -> None:
    repo = Repository(working_dir=tmp_path)
    repo.initialize()
    assert repo.list_branches() == []
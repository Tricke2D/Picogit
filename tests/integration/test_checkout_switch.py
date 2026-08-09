"""
Integration test: checkout switching between branches.
"""

from pathlib import Path

from minigit.cli.commands.add_cmd import run_add
from minigit.cli.commands.branch_cmd import run_branch
from minigit.cli.commands.checkout_cmd import run_checkout
from minigit.cli.commands.commit_cmd import run_commit
from minigit.core.repository import Repository


def test_checkout_restores_correct_file_version(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    repo = Repository(working_dir=tmp_path)
    repo.initialize()

    # Create initial commit on main
    (tmp_path / "config.txt").write_text("version A")
    run_add("config.txt")
    run_commit("commit on main", author="dev")

    # Create and switch to feature branch
    run_branch("feature")
    run_checkout("feature")

    # Change file on feature branch
    (tmp_path / "config.txt").write_text("version B")
    run_add("config.txt")
    run_commit("commit on feature", author="dev")

    # Switch back to main
    run_checkout("main")

    # Verify file is restored to version A
    assert (tmp_path / "config.txt").read_text() == "version A"
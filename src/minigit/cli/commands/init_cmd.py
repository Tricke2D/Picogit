"""
Initialize a new Mini Git repository.
"""

from pathlib import Path

from minigit.core.repository import Repository


def run_init() -> None:
    repo = Repository(working_dir=Path.cwd())
    if repo.is_initialized():
        print("Repository already initialized")
        return
    repo.initialize()
    print("Initialized empty Mini Git repository in .minigit/")
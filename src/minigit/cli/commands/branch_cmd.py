"""
Branch commands - list and create branches.
"""

from pathlib import Path

from minigit.core.repository import Repository


def run_branch(branch_name: str | None = None) -> list[str] | None:
    """Create a new branch if branch_name given, or list branches if not."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    if branch_name is None:
        return repo.list_branches()

    # Check if branch already exists
    if branch_name in repo.list_branches():
        raise ValueError(f"Branch '{branch_name}' already exists")

    repo.create_branch(branch_name)
    print(f"Created branch '{branch_name}'")
    return None
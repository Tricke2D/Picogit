"""
Show diff between staged and working file.
"""

from pathlib import Path

from minigit.core.diff import DiffOpType, compute_line_diff
from minigit.core.index import Index
from minigit.core.object_store import ObjectStore
from minigit.core.objects.blob import Blob
from minigit.core.repository import Repository


def run_diff(file_path: str) -> str:
    """Show diff between staged and working file."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)
    index = Index.load(repo.index_file)

    absolute_path = Path(file_path).resolve()
    relative_path = str(absolute_path.relative_to(repo.working_dir))

    staged_hash = index.entries.get(relative_path)
    staged_lines = (
        Blob.load(store, staged_hash).content.decode().splitlines()
        if staged_hash else []
    )
    working_lines = absolute_path.read_text().splitlines()

    ops = compute_line_diff(staged_lines, working_lines)

    output_lines = []
    for op in ops:
        if op.op_type == DiffOpType.EQUAL:
            output_lines.append(f"  {op.line}")
        elif op.op_type == DiffOpType.DELETE:
            output_lines.append(f"- {op.line}")
        else:
            output_lines.append(f"+ {op.line}")

    return "\n".join(output_lines)
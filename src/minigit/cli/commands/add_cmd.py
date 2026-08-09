"""
Add file to staging area.
"""

from pathlib import Path

from minigit.core.index import Index
from minigit.core.object_store import ObjectStore
from minigit.core.objects.blob import Blob
from minigit.core.repository import Repository


def run_add(file_path: str) -> None:
    """Stage a file to the index."""
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)
    index = Index.load(repo.index_file)

    absolute_path = Path(file_path).resolve()
    relative_path = str(absolute_path.relative_to(repo.working_dir))

    blob = Blob(content=absolute_path.read_bytes())
    blob_hash = blob.save(store)

    index.add(relative_path, blob_hash)
    index.save(repo.index_file)
    print(f"Added '{relative_path}' to staging area")
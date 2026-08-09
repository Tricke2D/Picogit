"""
Hash a file and store it as a blob.
"""

from pathlib import Path

from minigit.core.object_store import ObjectStore
from minigit.core.objects.blob import Blob
from minigit.core.repository import Repository


def run_hash_object(file_path: str) -> str:
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)
    content = Path(file_path).read_bytes()
    blob = Blob(content=content)
    object_hash = blob.save(store)
    return object_hash
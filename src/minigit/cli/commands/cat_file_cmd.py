"""
Display object content by hash.
"""

from pathlib import Path

from minigit.core.object_store import ObjectStore
from minigit.core.objects.blob import Blob
from minigit.core.repository import Repository


def run_cat_file(object_hash: str) -> bytes:
    repo = Repository(working_dir=Path.cwd())
    if not repo.is_initialized():
        raise RuntimeError("Not a Mini Git repository")

    store = ObjectStore(objects_dir=repo.objects_dir)
    blob = Blob.load(store, object_hash)
    return blob.content
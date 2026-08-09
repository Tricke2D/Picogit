from pathlib import Path

from minigit.core.object_store import ObjectStore
from minigit.core.objects.tree import Tree


def _make_sample_project(base: Path) -> None:
    (base / "README.md").write_text("hello")
    (base / "src").mkdir()
    (base / "src" / "main.py").write_text("print('hi')")


def test_tree_hash_is_deterministic(tmp_path: Path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")

    project_a = tmp_path / "project_a"
    project_a.mkdir()
    _make_sample_project(project_a)

    project_b = tmp_path / "project_b"
    project_b.mkdir()
    _make_sample_project(project_b)

    tree_a = Tree.build_from_directory(project_a, store)
    tree_b = Tree.build_from_directory(project_b, store)

    assert tree_a.serialize() == tree_b.serialize()


def test_tree_roundtrip_restores_identical_files(tmp_path: Path) -> None:
    store = ObjectStore(objects_dir=tmp_path / "objects")
    source = tmp_path / "source"
    source.mkdir()
    _make_sample_project(source)

    tree = Tree.build_from_directory(source, store)
    tree_hash = tree.save(store)

    restored_tree = Tree.load(store, tree_hash)
    restore_target = tmp_path / "restored"
    restored_tree.restore_to_directory(restore_target, store)

    assert (restore_target / "README.md").read_text() == "hello"
    assert (restore_target / "src" / "main.py").read_text() == "print('hi')"
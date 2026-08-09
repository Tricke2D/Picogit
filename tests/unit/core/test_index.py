from pathlib import Path

from minigit.core.index import Index


def test_index_add_then_save_and_load_roundtrip(tmp_path: Path) -> None:
    index_path = tmp_path / "index"
    index = Index()
    index.add("README.md", "abc123")
    index.add("src/main.py", "def456")
    index.save(index_path)

    loaded = Index.load(index_path)
    assert loaded.entries == {"README.md": "abc123", "src/main.py": "def456"}


def test_index_remove_deletes_entry(tmp_path: Path) -> None:
    index = Index()
    index.add("file.txt", "hash1")
    index.remove("file.txt")
    assert "file.txt" not in index.entries


def test_index_load_empty_file_returns_empty_index(tmp_path: Path) -> None:
    index_path = tmp_path / "index"
    index_path.write_text("")
    loaded = Index.load(index_path)
    assert loaded.entries == {}
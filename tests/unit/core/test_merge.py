from minigit.core.merge import merge_file


def test_merge_file_no_conflict() -> None:
    base = ["line 1", "line 2", "line 3"]
    head = ["line 1 CHANGED", "line 2", "line 3"]
    incoming = ["line 1", "line 2", "line 3 CHANGED"]

    merged, has_conflict = merge_file(base, head, incoming)

    assert not has_conflict
    assert "line 1 CHANGED" in merged
    assert "line 3 CHANGED" in merged


def test_merge_file_conflict_on_same_line() -> None:
    base = ["line 1", "line 2", "line 3"]
    head = ["line 1 FROM HEAD", "line 2", "line 3"]
    incoming = ["line 1 FROM INCOMING", "line 2", "line 3"]

    merged, has_conflict = merge_file(base, head, incoming)

    assert has_conflict
    assert "<<<<<<< HEAD" in merged
    assert "=======" in merged
    assert ">>>>>>> incoming" in merged


def test_merge_file_head_only_change() -> None:
    base = ["line 1", "line 2", "line 3"]
    head = ["line 1 CHANGED", "line 2", "line 3"]
    incoming = ["line 1", "line 2", "line 3"]

    merged, has_conflict = merge_file(base, head, incoming)

    assert not has_conflict
    assert "line 1 CHANGED" in merged


def test_merge_file_incoming_only_change() -> None:
    base = ["line 1", "line 2", "line 3"]
    head = ["line 1", "line 2", "line 3"]
    incoming = ["line 1 CHANGED", "line 2", "line 3"]

    merged, has_conflict = merge_file(base, head, incoming)

    assert not has_conflict
    assert "line 1 CHANGED" in merged
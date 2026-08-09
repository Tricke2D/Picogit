from minigit.core.diff import DiffOpType, compute_line_diff


def test_identical_lines_are_all_equal() -> None:
    lines = ["a", "b", "c"]
    ops = compute_line_diff(lines, lines)
    assert all(op.op_type == DiffOpType.EQUAL for op in ops)


def test_changed_line_produces_delete_and_insert() -> None:
    a = ["line 1", "line 2", "line 3"]
    b = ["line 1", "line 2 CHANGED", "line 3"]
    ops = compute_line_diff(a, b)

    op_types = [op.op_type for op in ops]
    assert DiffOpType.DELETE in op_types
    assert DiffOpType.INSERT in op_types


def test_diff_against_empty_file_is_all_insert() -> None:
    ops = compute_line_diff([], ["new line 1", "new line 2"])
    assert all(op.op_type == DiffOpType.INSERT for op in ops)


def test_diff_empty_vs_empty() -> None:
    ops = compute_line_diff([], [])
    assert ops == []


def test_diff_delete_all_lines() -> None:
    a = ["line 1", "line 2"]
    b = []
    ops = compute_line_diff(a, b)
    assert all(op.op_type == DiffOpType.DELETE for op in ops)
    assert len(ops) == 2
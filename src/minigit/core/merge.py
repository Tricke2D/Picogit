"""
3-way merge algorithm - core of merge functionality.
"""

from dataclasses import dataclass

from minigit.core.diff import DiffOpType, compute_line_diff


@dataclass
class Hunk:
    """One group of changes: base range and new lines."""

    base_start: int
    base_end: int
    new_lines: list[str]


def _extract_hunks(ops: list) -> list[Hunk]:
    """Extract hunks from diff ops."""
    hunks: list[Hunk] = []
    base_index = 0
    pending_new: list[str] = []
    hunk_start: int | None = None

    def _flush() -> None:
        nonlocal hunk_start, pending_new
        if hunk_start is not None:
            hunks.append(Hunk(base_start=hunk_start, base_end=base_index, new_lines=pending_new))
        hunk_start = None
        pending_new = []

    for op in ops:
        if op.op_type == DiffOpType.EQUAL:
            _flush()
            base_index += 1
        elif op.op_type == DiffOpType.DELETE:
            if hunk_start is None:
                hunk_start = base_index
            base_index += 1
        else:  # INSERT
            if hunk_start is None:
                hunk_start = base_index
            pending_new.append(op.line)

    _flush()
    return hunks


def merge_file(base_lines: list[str], head_lines: list[str], incoming_lines: list[str]) -> tuple[list[str], bool]:
    """
    Perform 3-way merge on one file.
    Returns (merged_lines, has_conflict).
    """
    hunks_head = _extract_hunks(compute_line_diff(base_lines, head_lines))
    hunks_incoming = _extract_hunks(compute_line_diff(base_lines, incoming_lines))

    head_by_range = {(h.base_start, h.base_end): h for h in hunks_head}
    incoming_by_range = {(h.base_start, h.base_end): h for h in hunks_incoming}
    all_ranges = sorted(set(head_by_range) | set(incoming_by_range))

    merged: list[str] = []
    cursor = 0
    has_conflict = False

    for start, end in all_ranges:
        merged.extend(base_lines[cursor:start])

        head_hunk = head_by_range.get((start, end))
        incoming_hunk = incoming_by_range.get((start, end))

        if head_hunk and not incoming_hunk:
            merged.extend(head_hunk.new_lines)
        elif incoming_hunk and not head_hunk:
            merged.extend(incoming_hunk.new_lines)
        elif head_hunk and incoming_hunk and head_hunk.new_lines == incoming_hunk.new_lines:
            merged.extend(head_hunk.new_lines)
        else:
            has_conflict = True
            merged.append("<<<<<<< HEAD")
            merged.extend(head_hunk.new_lines if head_hunk else [])
            merged.append("=======")
            merged.extend(incoming_hunk.new_lines if incoming_hunk else [])
            merged.append(">>>>>>> incoming")

        cursor = end

    merged.extend(base_lines[cursor:])
    return merged, has_conflict
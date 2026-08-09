"""
Diff algorithm (LCS-based) for line-by-line comparison.
"""

from dataclasses import dataclass
from enum import Enum


class DiffOpType(Enum):
    EQUAL = "equal"
    DELETE = "delete"
    INSERT = "insert"


@dataclass
class DiffOp:
    """One diff operation."""
    op_type: DiffOpType
    line: str


def _longest_common_subsequence_table(a: list[str], b: list[str]) -> list[list[int]]:
    """Build LCS DP table."""
    rows, cols = len(a) + 1, len(b) + 1
    table = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])

    return table


def compute_line_diff(a: list[str], b: list[str]) -> list[DiffOp]:
    """Generate diff operations to transform a into b."""
    table = _longest_common_subsequence_table(a, b)
    ops: list[DiffOp] = []

    i, j = len(a), len(b)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            ops.append(DiffOp(DiffOpType.EQUAL, a[i - 1]))
            i, j = i - 1, j - 1
        elif j > 0 and (i == 0 or table[i][j - 1] >= table[i - 1][j]):
            ops.append(DiffOp(DiffOpType.INSERT, b[j - 1]))
            j -= 1
        else:
            ops.append(DiffOp(DiffOpType.DELETE, a[i - 1]))
            i -= 1

    ops.reverse()
    return ops
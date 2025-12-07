from librarium.sparse_arr import SparseArray
from pyaoc.input import parse_input_lines_as_columns
from pyaoc.solution import Solution

type ParsedInput = list[SparseArray[str]]


def _parse_sparse(input_lines: list[str]) -> tuple[ParsedInput, int]:
    start_col = None
    for i, c in enumerate(input_lines[0]):
        if c != "S":
            continue
        start_col = i
        input_lines[0] = input_lines[0][:i] + "." + input_lines[0][i + 1 :]
        break

    rows, cols = len(input_lines), len(input_lines[0])
    col_lines = parse_input_lines_as_columns(input_lines)
    sparse_columns = []
    for line in col_lines:
        assert len(line) == rows
        sparse_col = SparseArray.from_list(line, default_value=".")
        sparse_columns.append(sparse_col)
    assert len(sparse_columns) == cols
    assert start_col is not None
    return sparse_columns, start_col


def _run_tachyon_mainfold(sparse_columns: ParsedInput, start_col: int) -> int:
    total_splits, cur_row = 0, 0

    # Dict to preserve order of beams (left to right), but also column presence lookup
    beams = {start_col: True}
    total_rows = sparse_columns[0].length

    new_beams: dict[int, bool]
    min_row: int

    def _follow_the_beam(col: int) -> int:
        nonlocal new_beams, min_row

        sparse_col = sparse_columns[col]
        # If splitter is not found -- beam goes brrrrr
        splitter_row = sparse_col.next_from(cur_row)
        if splitter_row is None:
            return 0

        # The leftmost beam is always the minimal one in inputs
        if splitter_row < min_row:
            min_row = splitter_row
        # Do not go further than the minimum row found this iteration, to avoid duplicates
        elif splitter_row > min_row:
            new_beams[col] = True
            return 0

        # "Simple" split case, here we can count the split and add new beams
        left, right = col - 1, col + 1
        new_beams[left] = True
        new_beams[right] = True
        return 1

    while beams:
        new_beams, min_row = {}, total_rows
        for col in beams:
            if col in new_beams:  # No dups
                continue
            total_splits += _follow_the_beam(col)

        beams = new_beams
        cur_row = min_row

    return total_splits


def _run_quantum_tachyon_mainfold(sparse_columns: ParsedInput, start_col: int) -> int:
    total_rows = sparse_columns[0].length

    final_timelines = 0
    timelines = {start_col: 1}  # per column timelines
    cur_row = 0

    new_timelines: dict[int, int]
    min_row: int

    def _follow_the_timelines(col: int):
        nonlocal new_timelines, min_row, final_timelines

        sparse_col = sparse_columns[col]
        # If splitter is not found -- beam goes brrrrr
        splitter_row = sparse_col.next_from(cur_row)
        if splitter_row is None:
            final_timelines += timelines[col]
            return

        # The leftmost beam is always the minimal one in inputs
        if splitter_row < min_row:
            min_row = splitter_row
        # Do not go further than the minimum row found this iteration, to avoid duplicates
        elif splitter_row > min_row:
            new_timelines[col] = new_timelines.get(col, 0) + timelines[col]
            return

        # "Simple" case, here we can add incoming timelines to already existing ones
        left, right = col - 1, col + 1
        new_timelines[left] = new_timelines.get(left, 0) + timelines[col]
        new_timelines[right] = new_timelines.get(right, 0) + timelines[col]

    while timelines:
        new_timelines, min_row = {}, total_rows

        for col in timelines:
            # Do not process duplicate beams, just accumulate timelines
            if col in new_timelines:
                new_timelines[col] += timelines[col]
                continue
            _follow_the_timelines(col)

        cur_row = min_row
        timelines = new_timelines

    return final_timelines


class Solution250701(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 7
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        sparse_columns, start_col = _parse_sparse(input_lines)
        self.start_col = start_col
        return sparse_columns

    def solve(self) -> int:
        assert hasattr(self, "start_col")
        return _run_tachyon_mainfold(self.parsed_input, self.start_col)


class Solution250702(Solution250701):
    PART: int = 2

    def solve(self) -> int:
        assert hasattr(self, "start_col")
        return _run_quantum_tachyon_mainfold(self.parsed_input, self.start_col)


Solution250701.register()
Solution250702.register()

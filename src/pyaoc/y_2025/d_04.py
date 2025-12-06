from typing import Callable

from librarium.grid import FULL_GRID, Grid, Position
from pyaoc.input import parse_input_lines_as_chars
from pyaoc.solution import Solution

type ParsedInput = list[list[str]]


EMPTY_CELL = "."
PAPER_ROLL = "@"

INACCESSIBLE = 4


class Cell:
    def __init__(self, value: str):
        self.value = value
        self.neigh_count = 0

    def is_paper(self) -> bool:
        return self.value == PAPER_ROLL

    def empty(self):
        self.value = EMPTY_CELL
        self.neigh_count = 0

    def inc(self):
        if self.is_paper():
            self.neigh_count += 1

    def dec(self):
        if self.is_paper():
            self.neigh_count -= 1

    def is_accessible(self) -> bool:
        return self.is_paper() and self.neigh_count < INACCESSIBLE

    def __str__(self) -> str:
        return f"{self.value}"


DUMMY_CELL = Cell(EMPTY_CELL)


def _init_neighbor_count(grid: Grid[Cell]):
    for pos, val in grid:
        if not val.is_paper():
            continue
        for neighbor in grid.neighbors(pos, directions=FULL_GRID):
            grid.get(neighbor).inc()


def _remove_all_accessible(
    grid: Grid[Cell], initial_accessible: list[tuple[Position, Cell]]
) -> int:
    total = 0

    def _n_filter(c: Cell) -> bool:
        return c.is_paper()

    def _visit(add_to_q: Callable[[Position, Cell], None], v_pos: Position, cell: Cell):
        nonlocal total
        cell.empty()
        total += 1

        for pos, neighbor_cell in grid.neighbors_with_values_filter(
            pos=v_pos,
            predicate=_n_filter,
            directions=FULL_GRID,
        ):
            neighbor_cell.dec()
            if neighbor_cell.is_accessible():
                add_to_q(pos, neighbor_cell)

    grid.dfs(initial_accessible, _visit)
    return total


class Solution250401(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 4
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return parse_input_lines_as_chars(input_lines)

    def _prepare_grid(self) -> Grid[Cell]:
        rows, cols = len(self.parsed_input), len(self.parsed_input[0])
        grid = Grid[Cell](rows=rows, cols=cols, default_value=DUMMY_CELL)

        for r in range(rows):
            for c in range(cols):
                grid.set(Position(r, c), Cell(self.parsed_input[r][c]))

        return grid

    def solve(self) -> int:
        grid = self._prepare_grid()
        _init_neighbor_count(grid)
        accessible = 0
        for _, cell in grid:
            if cell.is_accessible():
                accessible += 1
        return accessible


class Solution250402(Solution250401):
    PART: int = 2

    def solve(self) -> int:
        grid = self._prepare_grid()
        _init_neighbor_count(grid)
        initial_accessible = []
        for pos, cell in grid:
            if cell.is_accessible():
                initial_accessible.append((pos, cell))
        return _remove_all_accessible(grid, initial_accessible)


Solution250401.register()
Solution250402.register()

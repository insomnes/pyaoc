from collections import deque
from io import StringIO
from typing import Callable, Generator, Iterable, Iterator, NamedTuple, Self, TypeVar


class Position(NamedTuple):
    row: int
    col: int


class PosDelta(NamedTuple):
    d_row: int
    d_col: int


UP = PosDelta(-1, 0)
DOWN = PosDelta(1, 0)
LEFT = PosDelta(0, -1)
RIGHT = PosDelta(0, 1)

GRID_DIRS = (UP, RIGHT, DOWN, LEFT)

UP_RIGHT = PosDelta(-1, 1)
UP_LEFT = PosDelta(-1, -1)
DOWN_RIGHT = PosDelta(1, 1)
DOWN_LEFT = PosDelta(1, -1)

DIAG = (UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT)

# All 8 directions:
# UP_LEFT UP UP_RIGHT
# LEFT    X   RIGHT
# D_LEFT DOWN DOWN_RIGHT
FULL_GRID = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)


T = TypeVar("T")


class Grid[T]:
    def __init__(self, *, rows: int, cols: int, default_value: T | Callable[[], T]) -> None:
        self.rows = rows
        self.cols = cols
        self._grid: list[tuple[Position, T]] = self._prepare_grid_base(default_value)
        self._grid_len = len(self._grid)

    def _prepare_grid_base(self, default_value: T | Callable[[], T]) -> list[tuple[Position, T]]:
        def _make_value() -> T:
            if isinstance(default_value, Callable):
                return default_value()
            return default_value

        return [(self.pos_from_idx(i), _make_value()) for i in range(self.rows * self.cols)]

    def valid_pos(self, pos: Position) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def to_idx(self, pos: Position) -> int:
        if not self.valid_pos(pos):
            raise IndexError("Position out of bounds")

        return pos.row * self.cols + pos.col

    def pos_from_idx(self, idx: int) -> Position:
        if not (0 <= idx < self.rows * self.cols):
            raise IndexError("Index out of bounds")

        row = idx // self.cols
        col = idx % self.cols
        return Position(row, col)

    def get(self, pos: Position) -> T:
        _, val = self._grid[self.to_idx(pos)]
        return val

    def set(self, pos: Position, value: T) -> None:
        self._grid[self.to_idx(pos)] = (pos, value)

    def neighbors(
        self, pos: Position, directions: Iterable[PosDelta] = GRID_DIRS
    ) -> Generator[Position, None, None]:
        for d_row, d_col in directions:
            neighbor = Position(pos.row + d_row, pos.col + d_col)
            if self.valid_pos(neighbor):
                yield neighbor

    def neighbors_with_values(
        self, pos: Position, directions: Iterable[PosDelta] = GRID_DIRS
    ) -> Generator[tuple[Position, T], None, None]:
        for d_row, d_col in directions:
            neighbor = Position(pos.row + d_row, pos.col + d_col)
            if self.valid_pos(neighbor):
                yield (neighbor, self.get(neighbor))

    def neigh_filter(
        self,
        pos: Position,
        predicate: Callable[[T], bool],
        directions: Iterable[PosDelta] = GRID_DIRS,
    ) -> Generator[Position, None, None]:
        for d_row, d_col in directions:
            neighbor = Position(pos.row + d_row, pos.col + d_col)
            if self.valid_pos(neighbor) and predicate(self.get(neighbor)):
                yield neighbor

    def neigh_values(
        self, pos: Position, directions: Iterable[PosDelta] = GRID_DIRS
    ) -> Generator[T, None, None]:
        for d_row, d_col in directions:
            neighbor = Position(pos.row + d_row, pos.col + d_col)
            if self.valid_pos(neighbor):
                yield self.get(neighbor)

    def neigh_values_filter(
        self,
        pos: Position,
        predicate: Callable[[T], bool],
        directions: Iterable[PosDelta] = GRID_DIRS,
    ) -> Generator[T, None, None]:
        for d_row, d_col in directions:
            neighbor = Position(pos.row + d_row, pos.col + d_col)
            if self.valid_pos(neighbor):
                val = self.get(neighbor)
                if predicate(val):
                    yield val

    def neighbors_with_values_filter(
        self,
        pos: Position,
        predicate: Callable[[T], bool],
        directions: Iterable[PosDelta] = GRID_DIRS,
    ) -> Generator[tuple[Position, T], None, None]:
        for d_row, d_col in directions:
            neighbor = Position(pos.row + d_row, pos.col + d_col)
            if self.valid_pos(neighbor):
                val = self.get(neighbor)
                if predicate(val):
                    yield (neighbor, val)

    @classmethod
    def from_values(cls, values: list[list[T]], default_value: T) -> Self:
        rows = len(values)
        cols = len(values[0]) if rows > 0 else 0
        grid = cls(rows=rows, cols=cols, default_value=default_value)

        for r in range(rows):
            for c in range(cols):
                grid.set(Position(r, c), values[r][c])

        return grid

    def __iter__(self) -> Iterator[tuple[Position, T]]:
        return iter(self._grid)

    def filter(self, predicate: Callable[[T], bool]) -> Generator[tuple[Position, T], None, None]:
        for position, value in self:
            if predicate(value):
                yield (position, value)

    def iter_positions(self) -> Iterable[Position]:
        def _generator():
            for i in range(self._grid_len):
                position, _ = self._grid[i]
                yield position

        return _generator()

    def iter_values(self) -> Iterable[T]:
        def _generator():
            for _, value in self:
                yield value

        return _generator()

    def to_string(
        self,
        mark: Position | None = None,
        mark_char: str = "X",
        val_formatter: Callable[[T], str] | None = None,
    ) -> str:
        buf = StringIO()
        val_formatter = val_formatter or (lambda v: str(v))
        for pos, val in self:
            if mark is not None and pos == mark:
                buf.write(mark_char)
            else:
                buf.write(val_formatter(val))
            if pos.col == self.cols - 1:  # End of row
                buf.write("\n")

        return buf.getvalue()

    def bfs(
        self,
        start_queue: list[tuple[Position, T]],
        visit_func: Callable[[Callable[[Position, T], None], Position, T], None],
    ) -> None:
        queue = deque(start_queue)
        in_queue = {start_pos for start_pos, _ in start_queue}

        def _add_to_queue(pos: Position, val: T) -> None:
            nonlocal in_queue
            nonlocal queue

            if pos not in in_queue:
                queue.append((pos, val))
                in_queue.add(pos)

        while queue:
            pos, val = queue.popleft()
            in_queue.remove(pos)
            visit_func(_add_to_queue, pos, val)

    def dfs(
        self,
        start_stack: list[tuple[Position, T]],
        visit_func: Callable[[Callable[[Position, T], None], Position, T], None],
    ) -> None:
        stack = start_stack[:]
        in_stack = {start_pos for start_pos, _ in start_stack}

        def _add_to_stack(pos: Position, val: T) -> None:
            if pos not in in_stack:
                stack.append((pos, val))
                in_stack.add(pos)

        while stack:
            pos, val = stack.pop()
            in_stack.remove(pos)
            visit_func(_add_to_stack, pos, val)

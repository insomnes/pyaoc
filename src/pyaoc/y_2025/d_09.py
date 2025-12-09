from typing import NamedTuple

from pyaoc.solution import Solution

type ParsedInput = list[Point]


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_str(cls, s: str) -> "Point":
        x_str, y_str = s.split(",")
        return cls(int(x_str), int(y_str))

    def deltas(self, other: "Point") -> tuple[int, int]:
        return other.x - self.x, other.y - self.y


def cross_product(a: Point, b: Point, c: Point) -> int:
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


# ..............
# .......#...#..
# ..............
# ..#....#......
# .....#..#.....
# ..#....#.#....
# ..............
# .........#.#..
# ..............
class GridConvexHull:
    points: list[Point]

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.points.sort()
        self.hull = []

    def compute_hull(self) -> list[Point]:
        lower = []
        for p in self.points:
            while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(self.points):
            while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        self.hull = lower[:-1] + upper[:-1]
        return self.hull

    # ..............
    # ..OOOOOOOOO_..
    # ..OOOOOOOOOO..
    # ..OOOOOOOOOO..
    # ..OOOOOOOOOO..
    # .._OOOOOOOOO..
    # ..............
    # .........#.#..
    # ..............
    def max_rect_area_p1(self) -> int:
        if not self.hull:
            self.compute_hull()

        max_area = 0
        n = len(self.hull)
        for i in range(n):
            main_pt = self.hull[i]
            for j in range(i + 1, n):
                other_pt = self.hull[j]
                dx, dy = main_pt.deltas(other_pt)
                area = (abs(dx) + 1) * (abs(dy) + 1)
                if area > max_area:
                    max_area = area
        return max_area


class Solution250901(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 9
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return [Point.from_str(line) for line in input_lines]

    def solve(self) -> int:
        hull = GridConvexHull(self.parsed_input)
        return hull.max_rect_area_p1()


class Solution250902(Solution250901):
    PART: int = 2


Solution250901.register()

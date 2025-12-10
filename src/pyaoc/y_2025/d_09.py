from collections import defaultdict
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

    def rect_mirrors(self, other: "Point") -> list["Point"]:
        return [
            Point(self.x, other.y),
            Point(other.x, self.y),
        ]


def cross_product(a: Point, b: Point, c: Point) -> int:
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


# ..............
# .......#...#..
# ..............
# ..#....#......
# ..............
# ..#......#....
# ..............
# .........#.#..
# ..............
class GridConvexHull:
    points: list[Point]

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.points.sort(key=lambda p: (p.x, p.y))
        self.hull = []
        self.perimeter_hull = set()

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
    def max_rect_area(self) -> int:
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

    def compute_perimeter_hull(self) -> set[Point]:
        perimeter_hull = set()
        ordered_hull = []
        points_by_x = defaultdict(list)
        self.points.sort(key=lambda p: (p.x, -p.y))
        for p in self.points:
            print(f"Sorting pts by x desc y: {p}")
            points_by_x[p.x].append(p)

        self.points_by_x = points_by_x
        for _, pts in points_by_x.items():
            for p in pts:
                if p not in perimeter_hull:
                    perimeter_hull.add(p)
                    ordered_hull.append(p)

        points_by_y = defaultdict(list)
        for p in self.points:
            points_by_y[p.y].append(p)
        self.points_by_y = points_by_y
        for _, pts in points_by_y.items():
            for p in pts:
                if p not in perimeter_hull:
                    perimeter_hull.add(p)
                    ordered_hull.append(p)
        self.hull = ordered_hull
        self.perimeter_hull = perimeter_hull
        return self.perimeter_hull

    # ..............
    # .......#XXX#..
    # .......XXXXX..
    # .._OOOOOOOXX..
    # ..OOOOOOOOXX..
    # ..OOOOOOO_XX..
    # .........xXX..
    # .........#X#..
    # ..............
    def max_rect_area_inside(self) -> int:
        if not self.perimeter_hull:
            self.compute_perimeter_hull()

        # 113753500 too low
        print(f"Perimeter hull pts: {self.hull}")
        max_area = 0
        n = len(self.hull)
        for i in range(n):
            main_pt = self.hull[i]
            for j in range(i + 1, n):
                other_pt = self.hull[j]
                if main_pt.x == other_pt.x or main_pt.y == other_pt.y:
                    print(f"Skipping aligned pts: {main_pt}, {other_pt}")
                    continue
                print(f"Considering pts: {main_pt}, {other_pt}")
                assert main_pt.x <= other_pt.x

                max_y = self.points_by_x[main_pt.x][-1].y
                min_y = self.points_by_x[main_pt.x][0].y
                if not (min_y <= other_pt.y <= max_y):
                    print(f"  Rejected by y-boundary: {min_y} <= {other_pt.y} <= {max_y}")
                    continue
                print(f"  Accepted by y-boundary: {min_y} <= {other_pt.y} <= {max_y}")
                dx, dy = main_pt.deltas(other_pt)
                print(f"  Accepted rectangle with deltas: {abs(dx) + 1}, {abs(dy)}")
                area = (abs(dx) + 1) * (abs(dy) + 1)
                if area > max_area:
                    print(f"!!!!New max area: {area} vs {max_area}")
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
        return hull.max_rect_area()


class Solution250902(Solution250901):
    PART: int = 2

    def solve(self) -> int:
        hull = GridConvexHull(self.parsed_input)
        return hull.max_rect_area_inside()


Solution250901.register()
Solution250902.register()

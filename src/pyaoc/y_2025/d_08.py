import heapq
from functools import partial
from math import ceil, log, sqrt
from typing import NamedTuple

from librarium.unionfind import UnionFind
from pyaoc.solution import Solution


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __str__(self) -> str:
        return f"({self.x},{self.y},{self.z})"


TOP_K_1 = 3

type DistHeap = list[tuple[float, tuple[Point, Point]]]
type ParsedInput = tuple[DistHeap, list[Point]]


class Circuit:
    def __init__(self, points: list[Point]) -> None:
        self._points = set()
        self._supa_hash = 0
        for point in points:
            self.add_point(point)

    def add_point(self, point: Point) -> None:
        new_hash = self._supa_hash ^ hash(point)
        if new_hash == self._supa_hash:
            return
        self._supa_hash = new_hash
        self._points.add(point)

    def __hash__(self) -> int:
        return self._supa_hash

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circuit):
            return False
        return self._supa_hash == other._supa_hash

    def __contains__(self, item: object) -> bool:
        return item in self._points

    def __len__(self) -> int:
        return len(self._points)

    def __iter__(self):
        return iter(self._points)

    def __str__(self) -> str:
        return "{" + ", ".join(str(p) for p in sorted(self._points)) + "}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"


class Schema:
    def __init__(self, init_points: list[Point] | None = None) -> None:
        init_points = init_points if init_points is not None else []
        self._circuits: dict[Point, Circuit] = {p: Circuit([p]) for p in init_points}
        self.unique_circuits: dict[Circuit, int] = dict.fromkeys(self._circuits.values(), 1)

    def connect(self, p1: Point, p2: Point) -> bool:
        c1, c2 = self.ensure_circuit(p1), self.ensure_circuit(p2)
        if len(c2) > len(c1):
            c1, c2 = c2, c1
            p1, p2 = p2, p1
        if p1 in c2:
            return False
        if p2 in c1:
            assert p1 in c2
            return False

        self.remove_circ(c1)
        self.remove_circ(c2)

        for p in c2:
            c1.add_point(p)
            self._circuits[p] = c1
        self._circuits[p1] = c1
        self._circuits[p2] = c1

        self.add_circ(c1)
        return True

    def add_circ(self, circ: Circuit) -> None:
        self.unique_circuits[circ] = len(circ)

    def remove_circ(self, circ: Circuit) -> None:
        del self.unique_circuits[circ]

    def ensure_circuit(self, point: Point) -> Circuit:
        if point not in self._circuits:
            c = Circuit([point])
            self._circuits[point] = c
            self.add_circ(c)

        return self._circuits[point]


def _parse_input(input_lines: list[str]) -> tuple[DistHeap, list[Point]]:
    prev_points: list[Point] = []
    distances: DistHeap = []
    # N * log(N) edges is enough to build MST with very high probability
    # because MST is a subgraph of the Delaunay triangulation which has O(N) edges on average
    # and Delaunay triangulation is built from "close" points
    k_closest = ceil(log(len(input_lines)))
    print(f"Using k={k_closest} closest points out of {len(input_lines) - 1} total points")

    def _calc_dist(dp1: Point, dp2: Point) -> float:
        dx_sq, dy_sq, dz_sq = (dp1.x - dp2.x) ** 2, (dp1.y - dp2.y) ** 2, (dp1.z - dp2.z) ** 2
        return sqrt(dx_sq + dy_sq + dz_sq)

    for line in input_lines:
        point = Point(*[int(v) for v in line.split(",")])
        p_cd = partial(_calc_dist, point)

        for dist, exst_p in heapq.nsmallest(
            k_closest, zip(map(p_cd, prev_points), prev_points, strict=True)
        ):
            k1, k2 = (point, exst_p) if point < exst_p else (exst_p, point)
            heapq.heappush(distances, (dist, (k1, k2)))
        prev_points.append(point)
    return distances, prev_points


class Solution250801(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 8
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return _parse_input(input_lines)

    def solve(self) -> int:
        dist_heap, points = self.parsed_input
        schema = Schema(init_points=points)

        iters = 10 if self.with_sample else 1_000

        for _, (p1, p2) in heapq.nsmallest(iters, dist_heap):
            schema.connect(p1, p2)

        a, b, c = heapq.nlargest(
            TOP_K_1,
            schema.unique_circuits.items(),
            key=lambda item: item[1],
        )
        return a[1] * b[1] * c[1]


class Solution250802(Solution250801):
    PART: int = 2

    def solve_custom(self) -> int:
        dist_heap, points = self.parsed_input
        schema = Schema(init_points=points)

        p1, p2 = Point(0, 0, 0), Point(0, 0, 0)
        while len(schema.unique_circuits) > 1:
            _, (p1, p2) = heapq.heappop(dist_heap)
            schema.connect(p1, p2)

        return p1.x * p2.x

    def solve(self) -> int:
        dist_heap, points = self.parsed_input
        unfn = UnionFind(init_elements=points)

        p1, p2 = points[0], points[0]
        # In minimum spanning tree, we need exactly (N-1) edges to connect N points
        mst_edges = len(points) - 1
        total = 0
        while mst_edges:
            total += 1
            _, (p1, p2) = heapq.heappop(dist_heap)
            if unfn.union(p1, p2):
                mst_edges -= 1

        return p1.x * p2.x


Solution250801.register()
Solution250802.register()

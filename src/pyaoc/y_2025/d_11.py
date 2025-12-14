from collections import defaultdict
from functools import cached_property
from typing import Iterator

from pyaoc.solution import Solution

ORD_A = ord("a")


class Node:
    name: str
    parents: set["Node"]
    children: list["Node"]

    def __init__(self, name: str, parents: set["Node"], children: list["Node"]) -> None:
        self.name = name
        self.parents = parents
        self.children = children

    @cached_property
    def node_id(self) -> int:
        al, bl, cl = self.name
        a = (ord(al) - ORD_A) * 26 * 26
        b = (ord(bl) - ORD_A) * 26
        c = ord(cl) - ORD_A
        return a + b + c

    def add_parent(self, parent: "Node") -> None:
        self.parents.add(parent)

    def add_child(self, child: "Node") -> None:
        self.children.append(child)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.name == other.name

    def __str__(self) -> str:
        return f"Node({self.name})"

    def __repr__(self) -> str:
        return (
            f"Node({self.name}, parents={[p.name for p in self.parents]}, "
            f"children={[c.name for c in self.children]})"
        )


class DAG:
    nodes: dict[str, Node]

    def __init__(self) -> None:
        self.nodes = {}

    def ensure_node(self, name: str) -> Node:
        if name not in self.nodes:
            self.nodes[name] = Node(name=name, parents=set(), children=[])
        return self.nodes[name]

    def add_edge(self, parent_name: str, child_name: str) -> None:
        parent = self.ensure_node(parent_name)
        child = self.ensure_node(child_name)
        child.add_parent(parent)
        parent.add_child(child)

    def __iter__(self) -> Iterator[tuple[str, Node]]:
        return iter(self.nodes.items())

    def __contains__(self, name: str) -> bool:
        return name in self.nodes


type ParsedInput = DAG


def _parse_input(input_lines: list[str]) -> ParsedInput:
    dag = DAG()
    for line in input_lines:
        parent, children_raw = line.split(": ")
        assert len(parent) == 3
        children = children_raw.split()
        if not children:
            raise ValueError(f"Node {parent} has no children.")
        for child in children:
            assert len(child) == 3
            dag.add_edge(parent, child)
    return dag


def _layers(dag: DAG, start: str, end: str) -> tuple[list[dict[Node, int]], dict[Node, int]]:
    assert start in dag
    assert end in dag

    layers: list[dict[Node, int]] = []
    visited: set[Node] = set()

    all_paths: dict[Node, int] = defaultdict(lambda: 0)

    current_layer: dict[Node, int] = {dag.nodes[start]: 1}
    while current_layer:
        layers.append(current_layer)
        next_layer: dict[Node, int] = defaultdict(lambda: 0)
        for node in current_layer:
            visited.add(node)

            for child in node.children:
                next_layer[child] += current_layer[node]
                all_paths[child] += current_layer[node]

        current_layer = next_layer

    return layers, all_paths


class Solution251101(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 11
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return _parse_input(input_lines)

    def solve(self) -> int:
        dag = self.parsed_input
        _, all_paths = _layers(dag, start="you", end="out")
        end_node = dag.nodes["out"]
        return all_paths[end_node]


SPECIAL_P2_SAMPLE = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".split("\n")[1:-1]  # noqa: SIM905


class Solution251102(Solution251101):
    PART: int = 2

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        actual_input_lines = SPECIAL_P2_SAMPLE.copy() if self.with_sample else input_lines
        return super()._parse_input(actual_input_lines)

    def solve(self) -> int:
        dag = self.parsed_input
        _, fft_paths = _layers(dag, start="svr", end="fft")
        fft_node = dag.nodes["fft"]
        fft_cnt = fft_paths[fft_node]

        _, dac_paths = _layers(dag, start="fft", end="dac")
        dac_node = dag.nodes["dac"]
        dac_cnt = dac_paths[dac_node]

        _, out_paths = _layers(dag, start="dac", end="out")
        out_node = dag.nodes["out"]
        out_cnt = out_paths[out_node]

        print(f"Paths to fft: {fft_cnt}, fft -> dac: {dac_cnt}, dac -> out: {out_cnt}")

        return fft_cnt * dac_cnt * out_cnt


Solution251101.register()
Solution251102.register()

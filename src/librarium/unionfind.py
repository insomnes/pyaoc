"""
Uninon-Find (Disjoint Set Union):
Helpful in tasks that involve grouping elements and checking connectivity.

Main idea:
- Each element points to a parent, forming a tree structure.
- When we union two sets, we link the root of one tree to the root of another.
- Path compression is used during the find operation to flatten the structure,
  improving efficiency for future operations.
"""

from typing import Hashable, TypeVar

T = TypeVar("T", bound=Hashable)


class UnionFind[T]:
    def __init__(self, init_elements: list[T]) -> None:
        self.roots: dict[T, T] = {elem: elem for elem in init_elements}
        self.size: dict[T, int] = dict.fromkeys(init_elements, 1)

    def add_element(self, value: T) -> None:
        if value not in self.roots:
            self.roots[value] = value
            self.size[value] = 1

    def find_root(self, value: T) -> T:
        # Flatten the tree structure until we reach the root
        root = value
        while self.roots[root] != root:
            root = self.roots[root]

        while value != root:
            parent = self.roots[value]
            self.roots[value] = root
            value = parent

        return root

    def union(self, val_a: T, val_b: T) -> bool:
        root_a, root_b = self.find_root(val_a), self.find_root(val_b)
        if root_a == root_b:
            return False

        # Bigger fish eats smaller one (unionization is size-based)
        size_a, size_b = self.size[root_a], self.size[root_b]
        if size_a < size_b:
            root_a, root_b = root_b, root_a
            size_a, size_b = size_b, size_a

        self.roots[root_b] = root_a
        self.size[root_a] += size_b
        return True


class SimpleUNF(UnionFind[int]):
    def __init__(self, init_elements: list[int] | None, size: int = 0) -> None:
        init_elements = init_elements if init_elements is not None else list(range(size))
        self.roots: list[int] = list(init_elements)  # type: ignore
        self.size: list[int] = [1] * len(init_elements)  # type: ignore

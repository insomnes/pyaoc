import bisect
from typing import Self, TypeVar

T = TypeVar("T")


class SparseArray[T]:
    def __init__(self, length: int, default_value: T):
        self.data = {}
        self.keys = []
        self.default_value = default_value
        self.length = length

    def set(self, index: int, value: T):
        if value != self.default_value:
            if index not in self.data:
                bisect.insort_right(self.keys, index)
            self.data[index] = value
            return

        if index not in self.data:
            return

        del self.data[index]
        i = bisect.bisect_left(self.keys, index)
        self.keys.pop(i)

    def get(self, index: int) -> T:
        return self.data.get(index, self.default_value)

    def prev_from(self, index: int) -> int | None:
        i = bisect.bisect_left(self.keys, index) - 1
        if i < 0:
            return None
        return self.keys[i]

    def next_from(self, index: int) -> int | None:
        i = bisect.bisect_right(self.keys, index)
        if i >= len(self.keys):
            return None
        return self.keys[i]

    def __repr__(self):
        return f"SparseArray({self.data})"

    @classmethod
    def from_list(cls, lst: list[T], default_value: T) -> Self:
        sparse_array = cls(length=len(lst), default_value=default_value)
        for i, v in enumerate(lst):
            if v != default_value:
                sparse_array.set(i, v)
        return sparse_array

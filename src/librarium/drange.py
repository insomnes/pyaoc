class DynamicRange:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def contains(self, value: int) -> bool:
        return self.start <= value <= self.end

    def __repr__(self):
        return f"DynamicRange({self.start}, {self.end})"

    def merge(self, other: "DynamicRange") -> "DynamicRange":
        if not self.intersects(other):
            raise ValueError("Ranges do not overlap and cannot be merged")
        new_start = min(self.start, other.start)
        new_end = max(self.end, other.end)
        return DynamicRange(new_start, new_end)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DynamicRange):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __contains__(self, value: int) -> bool:
        return self.start <= value <= self.end

    def intersects(self, other: "DynamicRange") -> bool:
        return not (self.end < other.start or self.start > other.end)


def merge_overlapping_ranges(ranges: list[DynamicRange]) -> list[DynamicRange]:
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    merged_ranges = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last_merged = merged_ranges[-1]
        if last_merged.intersects(current):
            merged_ranges[-1] = last_merged.merge(current)
        else:
            merged_ranges.append(current)

    return merged_ranges


class MultiRange:
    def __init__(self):
        self._ranges = []

    @classmethod
    def from_ranges(cls, ranges: list[DynamicRange]) -> "MultiRange":
        mr = cls()
        merged = merge_overlapping_ranges(ranges)
        mr._ranges = merged
        return mr

    @property
    def total_covered(self) -> int:
        total = 0
        for drange in self._ranges:
            total += drange.end - drange.start + 1
        return total

    def contains(self, value: int) -> bool:
        return any(value in drange for drange in self._ranges)

    def __repr__(self):
        return f"MultiRange({self._ranges})"

    def __contains__(self, value: int) -> bool:
        return any(value in drange for drange in self._ranges)

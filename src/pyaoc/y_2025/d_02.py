from dataclasses import dataclass
from functools import cached_property

from pyaoc.solution import Solution


@dataclass
class IDRange:
    start: int
    end: int

    s_len: int
    e_len: int

    @classmethod
    def from_string(cls, s: str) -> "IDRange":
        """11-22 or 95-115 or 1023-1045"""
        start_str, end_str = s.split("-")
        start = int(start_str)
        end = int(end_str)
        return cls(start=start, s_len=len(start_str), end=end, e_len=len(end_str))

    @cached_property
    def is_simple_even(self) -> bool:
        if self.s_len == self.e_len:
            return self.s_len % 2 == 0
        return False

    @cached_property
    def can_be_evenized(self) -> bool:
        norm = self.s_len % 2 == 0 or self.e_len % 2 == 0
        return norm

    def evenized(self) -> "IDRange":
        """
        Return an evenized version of this IDRange, depending on if start or end
        is even length.
        """

        if not self.can_be_evenized:
            raise ValueError("Cannot normalize an IDRange with both lengths odd")
        if self.s_len % 2 == 0:
            new_start = self.start
            new_end = (10 ** self.s_len) - 1
            new_len = self.s_len

        else:
            new_start = 10 ** self.s_len
            new_end = self.end
            new_len = self.e_len
        return IDRange(
            start=new_start,
            end=new_end,
            s_len=new_len,
            e_len=new_len,
        )




type ParsedInput = list[IDRange]


def find_invalid_p1(idr: IDRange) -> list[int]:
    n_len = idr.s_len
    div = 10 ** (n_len // 2)

    n_start = idr.start // div
    n_end = idr.end // div

    nums = []
    for n in range(n_start, n_end + 1):
        mirror = n * div + n
        if idr.start <= mirror <= idr.end:
            nums.append(mirror)

    return nums






class Solution250201(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 2
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        assert len(input_lines) == 1, "Non 1 input lines?"
        return [IDRange.from_string(s) for s in input_lines[0].split(",")]

    def solve(self) -> int:
        all_nums = []
        for idr in self.parsed_input:
            if idr.is_simple_even:
                all_nums.extend(find_invalid_p1(idr))
            elif idr.can_be_evenized:
                normalized_idr = idr.evenized()
                if not normalized_idr.is_simple_even:
                    continue
                all_nums.extend(find_invalid_p1(normalized_idr))
        assert len(all_nums) == len(set(all_nums)), "Duplicates in all_nums?"
        return sum(all_nums)


Solution250201.register()

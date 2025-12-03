from dataclasses import dataclass
from functools import cached_property, lru_cache

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
    def has_eq_lengths(self) -> bool:
        return self.s_len == self.e_len

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
            new_end = (10**self.s_len) - 1
            new_len = self.s_len

        else:
            new_start = 10**self.s_len
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
    """
    Invalid ids are made only of some sequence of digits repeated twice.
    So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.
    """
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


def find_invalid_p2(idr: IDRange) -> set[int]:  # noqa: C901
    """
    Now invalid ids are made only of some sequence of digits repeated at least twice.
    So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times),
    and 1111111 (1 seven times) are all invalid IDs.
    """
    if idr.has_eq_lengths:
        min_repeats = next(i for i in range(2, idr.s_len + 1) if idr.s_len % i == 0)
    else:
        s_min = next((i for i in range(2, idr.s_len + 1) if idr.s_len % i == 0), idr.s_len + 1)
        e_min = next((i for i in range(2, idr.e_len + 1) if idr.e_len % i == 0), idr.e_len + 1)
        min_repeats = min(s_min, e_min)

    nums = set()

    @lru_cache
    def check_repeats(r: int, num: int) -> bool:
        nonlocal nums
        rep_num, pow_mul = num, 10 ** (len(str(num)))

        for _ in range(r - 1):
            rep_num = rep_num * pow_mul + num
        if rep_num > idr.end:
            return False
        if idr.start <= rep_num <= idr.end:
            nums.add(rep_num)
        return True

    max_repeats = idr.s_len if idr.has_eq_lengths else idr.e_len

    @lru_cache
    def find_invalids_in_range(start: int, end: int, reps: int) -> None:
        s_len = len(str(start))
        n_start, n_end = start, end
        p_mul = 10 ** (s_len // reps)

        for _ in range(reps - 1):
            n_start = n_start // p_mul
            n_end = n_end // p_mul

        for n in range(n_start, n_end + 1):
            if not check_repeats(reps, n):
                break

    for r in range(min_repeats, max_repeats + 1):
        if idr.s_len % r != 0 and idr.e_len % r != 0:
            continue

        if idr.has_eq_lengths:
            find_invalids_in_range(idr.start, idr.end, r)
            continue

        if idr.s_len % r == 0:
            new_start = idr.start
            new_end = (10**idr.s_len) - 1
        elif idr.e_len % r == 0:
            new_start = 10**idr.s_len
            new_end = idr.end
        else:
            raise RuntimeError("Should not be here")

        find_invalids_in_range(new_start, new_end, r)

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


class Solution250202(Solution250201):
    PART: int = 2

    def solve(self) -> int:
        all_nums = set()
        for idr in self.parsed_input:
            invalids = find_invalid_p2(idr)
            all_nums.update(invalids)
        return sum(all_nums)


Solution250201.register()
Solution250202.register()

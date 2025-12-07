from librarium.drange import DynamicRange, MultiRange
from pyaoc.input import parse_input_lines_as_ints
from pyaoc.solution import Solution

type ParsedInput = tuple[MultiRange, list[int]]


def _parse_ranges(input_lines: list[str]) -> list[DynamicRange]:
    ranges = []
    for line in input_lines:
        start_str, end_str = line.split("-")
        ranges.append(DynamicRange(int(start_str), int(end_str)))
    return ranges


def _parse_inp(input_lines: list[str]) -> ParsedInput:
    br_point = None
    for i, line in enumerate(input_lines):
        if line.strip() == "":
            br_point = i
            break

    if br_point is None:
        raise ValueError("No blank line separating ranges and numbers")

    ranges = _parse_ranges(input_lines[:br_point])
    numbers = parse_input_lines_as_ints(input_lines[br_point + 1 :])
    m_range = MultiRange.from_ranges(ranges)
    return m_range, numbers


class Solution250501(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 5
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return _parse_inp(input_lines)

    def solve(self) -> int:
        m_range, numbers = self.parsed_input
        count = 0
        for n in numbers:
            if n in m_range:
                count += 1
        return count


class Solution250502(Solution250501):
    PART: int = 2

    def solve(self) -> int:
        m_range, _ = self.parsed_input
        total_covered = m_range.total_covered
        return total_covered


Solution250501.register()
Solution250502.register()

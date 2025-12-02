from pyaoc.input import parse_input_lines_as_ints
from pyaoc.solution import Solution

LOOKUP = 2020

type ParsedInput = list[int]


def _to_lookup(vals: list[int], lookup: int) -> int | None:
    for i, x in enumerate(vals):
        for y in vals[i + 1 :]:
            if x + y == lookup:
                return x * y

    return None


class Solution200101(Solution[ParsedInput]):
    YEAR: int = 2020
    DAY: int = 1
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return parse_input_lines_as_ints(input_lines)

    def solve(self) -> int:
        result = _to_lookup(self.parsed_input, LOOKUP)
        if result is not None:
            return result
        raise ValueError("No solution found.")

class Solution200102(Solution200101):
    PART: int = 2

    def solve(self) -> int:
        for i, x in enumerate(self.parsed_input):
            target = LOOKUP - x
            result = _to_lookup(self.parsed_input[i + 1 :], target)
            if result is not None:
                return x * result
        raise ValueError("No solution found.")

Solution200101.register()
Solution200102.register()

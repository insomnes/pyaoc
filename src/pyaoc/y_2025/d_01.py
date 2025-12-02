from librarium.modclock import CountMode, ModClock
from pyaoc.solution import Solution

START = 50
BASE = 100
LOOKUP = 0

type ParsedInput = list[int]

class Solution250101(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 1
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        parsed: ParsedInput = []

        parsed = [
            int(line.strip()[1:]) if line.startswith("R") else -int(line[1:])
            for line in input_lines
        ]

        return parsed

    def solve(self) -> int:
        mod_clock = ModClock.from_parameters(
            start=START,
            modulus=BASE,
            count_mode=CountMode.EXACT,
            to_look_up=0,
        )
        mod_clock.make_moves(self.parsed_input)
        return mod_clock.counter


class Solution250102(Solution250101):
    PART: int = 2

    def solve(self) -> int:
        mod_clock = ModClock.from_parameters(
            start=START,
            modulus=BASE,
            count_mode=CountMode.CROSSING,
            to_look_up=0,
        )
        mod_clock.make_moves(self.parsed_input)
        return mod_clock.counter

Solution250101.register()
Solution250102.register()

from pyaoc.solution import Solution

type ParsedInput = list[str]


class Op:
    def __init__(self, raw: str) -> None:
        if raw == "+":
            self.action = "add"
            self.value = 0
        elif raw == "*":
            self.action = "mul"
            self.value = 1
        else:
            raise ValueError(f"Unknown operation: {raw}")

    def _add(self, x: int):
        self.value += x

    def _mul(self, x: int):
        self.value *= x

    def execute(self, val: int):
        if self.action == "add":
            self._add(val)
        elif self.action == "mul":
            self._mul(val)
        else:
            raise ValueError(f"Unknown operation: {self.action}")


class Solution250601(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 6
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return input_lines

    def solve(self) -> int:
        operations = [Op(v.strip()) for v in self.parsed_input[-1].split(" ") if v.strip()]
        for line in self.parsed_input[:-1]:
            parts = [int(v.strip()) for v in line.strip().split(" ") if v.strip()]
            assert len(parts) == len(operations)
            for i, val in enumerate(parts):
                operations[i].execute(val)
        return sum(op.value for op in operations)


class Solution250602(Solution250601):
    PART: int = 2

    def solve(self) -> int:
        return -1


Solution250601.register()

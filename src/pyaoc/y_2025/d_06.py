from pyaoc.solution import Solution

type ParsedInput = list[str]  # We don't want to parse it here


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


def _parse_operations(line: str) -> list[Op]:
    return [Op(v.strip()) for v in line.split(" ") if v.strip()]


class Solution250601(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 6
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return input_lines

    def solve(self) -> int:
        operations = _parse_operations(self.parsed_input[-1])
        for line in self.parsed_input[:-1]:
            parts = [int(v.strip()) for v in line.strip().split(" ") if v.strip()]
            assert len(parts) == len(operations)
            for i, val in enumerate(parts):
                operations[i].execute(val)
        return sum(op.value for op in operations)


class Solution250602(Solution250601):
    PART: int = 2

    def solve(self) -> int:
        operations = _parse_operations(self.parsed_input[-1])
        n_rows, n_cols = len(self.parsed_input) - 1, len(self.parsed_input[0])
        op_idx = -1
        cur_num = 0

        for col in range(n_cols - 1, -1, -1):
            for row in range(n_rows):
                char = self.parsed_input[row][col]
                if char == " ":
                    continue
                v = int(char)
                cur_num = cur_num * 10 + v

            if cur_num == 0:  # All ' ' in this col
                op_idx -= 1
                continue

            operations[op_idx].execute(cur_num)
            cur_num = 0

        return sum(op.value for op in operations)


Solution250601.register()
Solution250602.register()

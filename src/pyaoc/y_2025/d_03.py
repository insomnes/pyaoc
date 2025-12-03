from array import array

from pyaoc.input import parse_input_lines_as_lists_of_ints
from pyaoc.solution import Solution

type ParsedInput = list[list[int]]


def find_max_jolt_in_row(row: list[int]) -> int:
    f_jolt, s_jolt = row[0], -1
    for i in range(1, len(row)):
        n = row[i]
        if n > f_jolt and i < len(row) - 1:
            f_jolt, s_jolt = n, -1
        elif n > s_jolt:
            s_jolt = n

        if (f_jolt, s_jolt) == (9, 9):
            break

    return f_jolt * 10 + s_jolt


def find_max_jolt_in_row_digits(row: list[int], digits: int, jolts: array[int]) -> int:
    r_len = len(row)
    len_delta = digits - r_len
    default_s = 0
    for i in range(r_len):
        if default_s >= digits:
            break
        n = row[i]

        # Slide start index based on how many digits are left in the row
        # i=0 -> s=0
        # jolts [_ _ _]
        # row   [0 1 2 3 4 5]
        # i=1 -> s=0
        # ...
        # i=3 -> s=1
        # jolts  - - - [X _ _]
        # row   [0 1 2 3 4 5]
        # ...
        # i=4 -> s=2
        # jolts  - - - [X X _]
        # row   [0 1 2 3 4 5]

        s = default_s if i + digits < r_len else max(len_delta + i, default_s)

        for j in range(s, digits):
            if n <= jolts[j]:
                continue

            jolts[j] = n
            if j == default_s and n == 9:
                default_s += 1
            for jn in range(j + 1, digits):
                jolts[jn] = 0
                if jn + 1 < digits and jolts[jn + 1] == 0:
                    break
            break

    r_num = 0
    for jolt in jolts:
        r_num = r_num * 10 + jolt

    return r_num


class Solution250301(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 3
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return parse_input_lines_as_lists_of_ints(input_lines)

    def solve(self) -> int:
        total = 0
        jolts = array("b", [0, 0])

        def reset_jolts():
            nonlocal jolts

            jolts[0] = 0
            jolts[1] = 0

        for line in self.parsed_input:
            found = find_max_jolt_in_row_digits(line, 2, jolts)
            total += found
            reset_jolts()

        return total


class Solution250302(Solution250301):
    PART: int = 2

    def solve(self) -> int:
        total = 0
        digits = 12
        jolts = array("b", [0] * digits)

        def reset_jolts():
            nonlocal jolts

            for i in range(digits):
                jolts[i] = 0

        for line in self.parsed_input:
            found = find_max_jolt_in_row_digits(line, digits, jolts)
            total += found
            reset_jolts()

        return total


Solution250301.register()
Solution250302.register()

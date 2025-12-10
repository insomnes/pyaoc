import re
from typing import NamedTuple

from pyaoc.solution import Solution


class Buttons(NamedTuple):
    raw_num: str
    bit_num: str
    num: int
    buttons: list[tuple[int, ...]]
    bit_masks_buttons: list[int]
    jolts: list[int]

    def __str__(self) -> str:
        buttons_str = [
            f"{btn} [{bin(bit_btn)[2:].zfill(len(self.bit_num))}]"
            for btn, bit_btn in zip(self.buttons, self.bit_masks_buttons, strict=True)
        ]
        return (
            f"Buttons(num={self.bit_num} ({self.num}), buttons={buttons_str}, jolts={self.jolts})"
        )


type ParsedInput = list[Buttons]


pattern = re.compile(
    r"^(?P<raw_num>\[[^\]]+\])\s+"
    r"(?P<buttons>(?:\([^)]*\)\s*)+)"
    r"(?P<jolts>\{[^}]+\})$"
)


def _parse_bit_mask(num_str: str, button: tuple[int, ...]) -> int:
    bitmask = 0
    length = len(num_str)
    for pos in button:
        bitmask |= 1 << (length - 1 - pos)
    return bitmask


def _parse_bit_masks(num_str: str, buttons: list[tuple[int, ...]]) -> list[int]:
    bit_buttons = []
    for btn in buttons:
        bitmask = _parse_bit_mask(num_str, btn)
        bit_buttons.append(bitmask)
    return bit_buttons


def _parse_input(input_lines: list[str]) -> ParsedInput:
    parsed: ParsedInput = []
    for line in input_lines:
        matches = pattern.match(line)
        if not matches:
            raise ValueError(f"Invalid input line: {line}")
        raw_num = matches.group("raw_num")
        bit_num = "".join("1" if c == "#" else "0" for c in raw_num[1:-1])
        num = int(bit_num, 2)
        buttons_str = matches.group("buttons").strip()
        buttons = [
            tuple(int(x) for x in btn_str.strip("()").split(",")) for btn_str in buttons_str.split()
        ]
        bit_masks_buttons = _parse_bit_masks(bit_num, buttons)

        jolts_str = matches.group("jolts")
        jolts = [int(x) for x in jolts_str.strip("{}").split(",")]

        parsed.append(
            Buttons(
                raw_num=raw_num,
                bit_num=bit_num,
                num=num,
                buttons=buttons,
                bit_masks_buttons=bit_masks_buttons,
                jolts=jolts,
            )
        )

    return parsed


class Solution251001(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 10
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return _parse_input(input_lines)

    def solve(self) -> int:
        for buttons in self.parsed_input:
            print(buttons)
        return 0


class Solution251002(Solution251001):
    PART: int = 2


Solution251001.register()

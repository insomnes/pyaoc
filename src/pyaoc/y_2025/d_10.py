import re
from collections import deque
from functools import lru_cache
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


def bitmask_bfs(target: int, bin_len: int, bit_masks: list[int]) -> int:
    max_states = 1 << bin_len
    distances = [-1] * max_states

    parent: list[int | None] = [None] * max_states
    parent_mask: list[int | None] = [None] * max_states

    start = 0
    distances[start] = 0
    q = deque([start])

    while q:
        state = q.popleft()
        cur_dist = distances[state]

        for mask in bit_masks:
            next_state = state ^ mask
            if distances[next_state] != -1:
                continue
            distances[next_state] = cur_dist + 1
            if next_state == target:
                return distances[next_state]
            parent[next_state] = state
            parent_mask[next_state] = mask
            q.append(next_state)

    raise RuntimeError("Not found")


@lru_cache
def _increase_joltage(jolts: tuple[int, ...], jolt_button: tuple[int, ...]) -> tuple[int, ...]:
    def _jolt_generator():
        for i, jolt in enumerate(jolts):
            if i in jolt_button:
                yield jolt + 1
            else:
                yield jolt

    res = tuple(_jolt_generator())
    assert len(res) == len(jolts)
    return res


@lru_cache
def _decrease_joltage(
    jolts: tuple[int, ...], jolt_button: tuple[int, ...], n: int = 1
) -> tuple[int, ...]:
    def _jolt_generator():
        for i, jolt in enumerate(jolts):
            if i in jolt_button:
                yield jolt - n
            else:
                yield jolt

    res = tuple(_jolt_generator())
    assert len(res) == len(jolts)
    return res


def _find_joltage_jolt_buttons(
    jolts: list[int], buttons: list[tuple[int, ...]]
) -> list[list[tuple[int, ...]]]:
    # indexes of buttons that can increase each jolt
    jolts_buttons: list[list[tuple[int, ...]]] = [[] for _ in jolts]
    for jolt_idx, _ in enumerate(jolts):
        j_buttons = [btn for i, btn in enumerate(buttons) if jolt_idx in btn]
        jolts_buttons[jolt_idx] = j_buttons
    return jolts_buttons


def _joltage_delta(j1: tuple[int, ...], j2: tuple[int, ...]) -> tuple[int, ...]:
    res = tuple(sorted((a - b for a, b in zip(j1, j2, strict=True)), reverse=True))
    return res


class Solution251001(Solution[ParsedInput]):
    YEAR: int = 2025
    DAY: int = 10
    PART: int = 1

    def _parse_input(self, input_lines: list[str]) -> ParsedInput:
        return _parse_input(input_lines)

    def solve(self) -> int:
        total_steps = 0
        for buttons in self.parsed_input:
            bin_len = len(buttons.bit_num)
            steps = bitmask_bfs(buttons.num, bin_len, buttons.bit_masks_buttons)
            total_steps += steps
        return total_steps


class Solution251002(Solution251001):
    PART: int = 2

    def solve(self) -> int:
        return -1


Solution251001.register()
Solution251002.register()

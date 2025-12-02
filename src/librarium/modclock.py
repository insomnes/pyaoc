from enum import StrEnum
from typing import Self


class PositionTracker:
    def __init__(self, *, start: int, modulus: int, to_look_up: int):
        self.cur = start

        if modulus <= 0:
            raise ValueError("Modulus must be a positive integer.")
        self.modulus = modulus

        to_look_up = to_look_up if to_look_up is not None else 0
        if not (0 <= to_look_up < modulus):
            raise ValueError("Look up point must be in the range [0, modulus).")
        self.to_look_up = to_look_up

        self.counter = 0

    def advance(self, step: int):
        self.cur = (self.cur + step) % self.modulus
        if self.cur == self.to_look_up:
            self.counter += 1

    def _reverse(self):
        self.cur = self.modulus - self.cur if self.cur != 0 else 0

    def regress(self, step: int):
        self._reverse()
        self.advance(abs(step))
        self._reverse()


class CrossingPositionTracker(PositionTracker):
    def advance(self, step: int):
        total = self.cur + step
        full_cycles = total // self.modulus
        self.counter += full_cycles
        self.cur = total % self.modulus



class CountMode(StrEnum):
    EXACT = "exact"
    CROSSING = "crossing"

COUNTERS: dict[str, type[PositionTracker]] = {
    CountMode.EXACT: PositionTracker,
    CountMode.CROSSING: CrossingPositionTracker,
}

class ModClock:
    def __init__(self, *, tracker: PositionTracker):
        self.tracker = tracker

    def make_moves(self, moves: list[int]) -> None:
        for move in moves:
            if move >= 0:
                self.tracker.advance(move)
            else:
                self.tracker.regress(abs(move))

    @property
    def counter(self) -> int:
        return self.tracker.counter

    def reset(self, pos_tracker: PositionTracker) -> None:
        self.tracker = pos_tracker

    @classmethod
    def from_parameters(
        cls,
        *,
        start: int,
        modulus: int,
        count_mode: CountMode,
        to_look_up: int | None = None,
    ) -> Self:
        to_look_up = to_look_up if to_look_up is not None else 0
        tracker_cls = COUNTERS[count_mode]
        tracker = tracker_cls(
            start=start,
            modulus=modulus,
            to_look_up=to_look_up,
        )
        return cls(tracker=tracker)




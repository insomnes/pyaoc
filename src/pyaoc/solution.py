from abc import ABC, abstractmethod
from typing import TypeVar

from pyaoc.input import read_input_file

ParsedInputT = TypeVar("ParsedInputT")


class Solution[ParsedInputT](ABC):
    YEAR: int
    DAY: int
    PART: int

    def __init__(self, input_lines: list[str], sample: bool) -> None:
        self._check_attributes()

        self.with_sample = sample
        self._input_lines = input_lines.copy()
        self.parsed_input = self._parse_input(self._input_lines)

    @abstractmethod
    def _parse_input(self, input_lines: list[str]) -> ParsedInputT:
        pass

    @abstractmethod
    def solve(self) -> int:
        pass

    @classmethod
    def _check_attributes(cls) -> None:
        if not all(hasattr(cls, attr) for attr in ("YEAR", "DAY", "PART")):
            raise NotImplementedError(
                "Subclasses must define YEAR and DAY and PART class attributes."
            )

    @classmethod
    def register(cls) -> None:
        cls._check_attributes()
        global SOLUTION_REGISTRY
        SOLUTION_REGISTRY.register(cls)


type SolKey = tuple[int, int, int]  # (year, day, part)


class SolutionRegistry:
    def __init__(self):
        self._registry: dict[SolKey, type[Solution]] = {}

    def register(self, solution_cls: type[Solution]) -> None:
        if not all(hasattr(solution_cls, attr) for attr in ("YEAR", "DAY", "PART")):
            raise ValueError("Solution class must have YEAR, DAY, and PART attributes.")
        key = (solution_cls.YEAR, solution_cls.DAY, solution_cls.PART)
        self._registry[key] = solution_cls

    def prepare_solution_instance(self, key: SolKey, sample: bool = False) -> Solution:
        solution_cls = self._registry[key]
        input_lines = read_input_file(solution_cls.YEAR, solution_cls.DAY, sample)
        return solution_cls(input_lines, sample)

    def get_solution(self, key: tuple[int, int, int]) -> type[Solution]:
        return self._registry[key]

    def get_year_solutions(self, year: int) -> dict[SolKey, type[Solution]]:
        return {k: v for k, v in self._registry.items() if k[0] == year}

    def all_years(self) -> list[int]:
        return sorted({year for year, _, _ in self._registry})

    def all_keys(self) -> list[SolKey]:
        return sorted(self._registry)

    def __contains__(self, key: SolKey) -> bool:
        return key in self._registry

    def __iter__(self):
        return iter(self._registry.items())

    def __len__(self) -> int:
        return len(self._registry)


SOLUTION_REGISTRY = SolutionRegistry()


def register(solution_cls: type[Solution]) -> None:
    global SOLUTION_REGISTRY
    SOLUTION_REGISTRY.register(solution_cls)

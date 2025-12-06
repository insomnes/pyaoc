from array import array
from pathlib import Path

from pyaoc.config import INPUTS_DIR

YEAR_TEMPLATE = "y_{year:04d}"
DAY_TEMPLATE = "d_{day:02d}"


def prepare_input_path(year: int, day: int, sample: bool = False) -> Path:
    year_name = YEAR_TEMPLATE.format(year=year)
    day_name = DAY_TEMPLATE.format(day=day)
    file_name = f"{day_name}.txt" if not sample else f"sample_{day_name}.txt"

    return INPUTS_DIR / year_name / file_name


def read_input_file(year: int, day: int, sample: bool = False) -> list[str]:
    input_path = prepare_input_path(year, day, sample)
    return input_path.read_text().splitlines()


def parse_input_lines_as_ints(input_lines: list[str]) -> list[int]:
    return [int(line.strip()) for line in input_lines]


def parse_line_as_ints(line: str, sep: str | None = None) -> list[int]:
    return (
        [int(part) for part in line.strip().split(sep)] if sep else [int(n) for n in line.strip()]
    )


def parse_line_as_int_arr(line: str, t_code: str, sep: str | None = None) -> array:
    init_ints = (
        (int(part) for part in line.strip().split(sep)) if sep else (int(n) for n in line.strip())
    )
    return array(t_code, init_ints)


def parse_input_lines_as_lists_of_ints(
    input_lines: list[str], sep: str | None = None
) -> list[list[int]]:
    return [parse_line_as_ints(line, sep) for line in input_lines]


def parse_input_lines_as_chars(input_lines: list[str]) -> list[list[str]]:
    return [list(line.strip()) for line in input_lines]

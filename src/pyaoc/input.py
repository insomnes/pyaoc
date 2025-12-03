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

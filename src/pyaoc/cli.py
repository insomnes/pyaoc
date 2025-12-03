from itertools import product

import click

from pyaoc.solution import SOLUTION_REGISTRY
from pyaoc.solver import Solver


@click.command()
@click.option(
    "--years",
    "-y",
    multiple=True,
    type=int,
    help="Years to run solutions for.",
)
@click.option(
    "--days",
    "-d",
    multiple=True,
    type=int,
    help="Days to run solutions for.",
    default=None,
)
@click.option(
    "--with-sample",
    "-s",
    is_flag=True,
    default=False,
    help="Whether to run solutions with sample input or actual input.",
)
def run(
    years: list[int],
    days: list[int] | None = None,
    with_sample: bool = True,
):
    print("Running the PyAOC CLI...")
    print(f"Requested years: {years}")
    print(f"Requested days: {days}")
    print(f"With sample input: {with_sample}")

    print(f"Available years in registry: {SOLUTION_REGISTRY.all_years()}")
    if years is None or len(years) == 0:
        print("No years specified, running all available years.")
        to_solve = SOLUTION_REGISTRY.all_keys()
    elif days is None or len(days) == 0:
        to_solve = [(year, day, part) for year in years for day in range(1, 26) for part in (1, 2)]
    else:
        to_solve = [(year, day, part) for year, day, part in product(years, days, (1, 2))]

    solver = Solver(to_solve=to_solve, with_sample=with_sample)
    solver.solve_all()

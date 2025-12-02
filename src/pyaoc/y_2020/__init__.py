from pyaoc.y_2020.d_01 import Solution200101

YEAR = 2020

for solution_cls in [Solution200101]:
    assert solution_cls.YEAR == YEAR, (
        f"Solution class {solution_cls.__name__} has incorrect YEAR attribute."
    )


__all__ = [
    "Solution200101",
]

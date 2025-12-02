from time import perf_counter

from pyaoc.solution import SOLUTION_REGISTRY, SolKey


class Solver:
    def __init__(self, to_solve: list[SolKey], with_sample: bool = True) -> None:
        self._to_solve = to_solve
        self._with_sample = with_sample
        self.registry = SOLUTION_REGISTRY

    def solve(self, key: SolKey) -> int:
        solution_instance = self.registry.prepare_solution_instance(
            key, sample=self._with_sample
        )
        print(f"Solving {key} using {type(solution_instance).__name__}...")
        return solution_instance.solve()

    def solve_all(self) -> None:
        results: dict[SolKey, int] = {}
        prev_year, prev_day, prev_part = -1, -1, -1

        for key in self._to_solve:
            if key not in self.registry:
                continue
            year, day, part = key
            if year != prev_year:
                print("=====================")
                print(f"===== YEAR {year} =====")
                print("=====================")
                prev_year = year

            if day != prev_day:
                print("------------------")
                print(f"----- DAY {day:02} -----")
                print("------------------")
                prev_day = day
                prev_part = -1
            if part != prev_part:
                print(f"---- PART {part} ----")
                prev_part = part
            if self._with_sample:
                print(">> Sample Input <<")
            else:
                print(">> Actual Input <<")
            start = perf_counter()
            result = self.solve(key)
            results[key] = result
            res = f"    Result: {result}    "
            cap = "_" * (len(res) + 4)
            bot = "-" * (len(res) + 4)
            print(cap)
            print(f"| {res} |")
            print(bot)

            total_time = perf_counter() - start
            print(f"Solved in {total_time:.6f} seconds.")

            if self._with_sample:
                print("<< Sample Input End >>")
            else:
                print("<< Actual Input End >>")


import csv
import functools
import math
import pathlib
import sys


def main(var: str) -> float:
    current_path = pathlib.Path().absolute()
    root_path = current_path.parent
    sys.path.append(str(root_path))
    import task2.task as task2

    csv_rows = task2.main(var)
    input_rows = [list(map(int, r)) for r in csv.reader(csv_rows.split(), delimiter=",")]

    size = len(input_rows[0])
    p_rows = [[e/(size-1) for e in r] for r in input_rows]

    entr = [functools.reduce(lambda acc, p: acc - p*math.log2(p), filter(lambda r: r > 0, r), 0.0) for r in p_rows]
    return sum(entr)

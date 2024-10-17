from itertools import chain
import json

import numpy as np


def build_ind_map(data: list[int | list[int]]):
    ind_map = {}
    for ind, el in enumerate(data):
        if isinstance(el, list):
            for e in el:
                ind_map[e] = ind
        else:
            ind_map[el] = ind
    return ind_map


def build_matrix(ind_map: dict[int, int], flat_arr: np.ndarray) -> np.ndarray:
    n = flat_arr.shape[0]
    result = np.identity(n, dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            a, b = flat_arr[i], flat_arr[j]
            if ind_map[a] == ind_map[b]:
                result[a-1, b-1] = 1
                result[b-1, a-1] = 1
                continue
            ind = (b-1, a-1) if ind_map[a] >= ind_map[b] else (a-1, b-1)
            result[ind] = 1
    return result


def build_matrix_by_json(json_str: str) -> np.ndarray:
    data = json.loads(json_str)
    flat_arr = np.array(list(chain.from_iterable(x if isinstance(x, list) else [x] for x in data)), dtype=int)
    ind_map = build_ind_map(data)
    result = build_matrix(ind_map, flat_arr)
    return result


def main(a_str: str, b_str: str) -> np.ndarray:
    a = build_matrix_by_json(a_str)
    b = build_matrix_by_json(b_str)
    matr = (a&b) | (a.T&b.T)
    ind = np.vstack(np.where(matr == 0)).T
    return ind[ind[:, 0] < ind[:, 1]] + 1


if __name__ == "__main__":
    a = "[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]"
    b = "[[1,2],[3,4,5],6,7,9,[8,10]]"
    c = "[3,[1,4],2,6,[5,7,8],[9,10]]"
    print(main(a, b))

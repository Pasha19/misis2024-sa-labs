import csv

import numpy as np


def main(csv_str: str) -> np.ndarray:
    reader = csv.reader(csv_str.strip().splitlines()[1:], delimiter=",")
    data = np.array([list(map(int, row[1:])) for row in reader])
    row_sum = np.sum(data, axis=1)
    total = np.sum(row_sum)
    p = data / total
    p_y = np.sum(p, axis=1)
    p_x = np.sum(p, axis=0)
    h = np.sum(-p * np.log2(p))
    h_x = np.sum(-p_x * np.log2(p_x))
    h_y = np.sum(-p_y * np.log2(p_y))
    p_x_y = data / row_sum[..., np.newaxis]
    h_x_y = p_y @ np.sum(-p_x_y * np.log2(p_x_y), axis=1)
    i_x_y = h_x - h_x_y
    return np.round(np.array([h, h_x, h_y, h_x_y, i_x_y]), 2)

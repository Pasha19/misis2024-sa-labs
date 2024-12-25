from typing import Callable

import json


def linear_by_points(x0: float, y0: float, x1: float, y1: float) -> Callable[[float], float]:
    def func(x: float) -> float:
        if x0 == x1:
            return y1
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return func


def func_by_points(points: list[list[int]]) -> Callable[[float], float]:
    p = list(zip(*points))
    px = p[0]
    py = p[1]
    f = [linear_by_points(px[i], py[i], px[i+1], py[i+1]) for i in range(3)]
    def func(x: float) -> float:
        if x < px[0]:
            return py[0]
        if x > px[3]:
            return py[3]
        if px[0] <= x < px[1]:
            return f[0](x)
        if px[1] <= x < px[2]:
            return f[1](x)
        return f[2](x)
    return func


def inv_linear_by_points(x0: float, y0: float, x1: float, y1: float) -> Callable[[float], float | None]:
    def func(y: float) -> float | None:
        if x0 == x1:
            if y == y0:
                return x0
            if y == y1:
                return x1
            return None
        if y0 == y1:
            if y == y0:
                return x1
            return None
        if y < min(y0, y1) or y > max(y0, y1):
            return None
        return x0 + (y - y0) * (x1 - x0) / (y1 - y0)
    return func


def inv_func_by_points(points: list[list[int]]) -> Callable[[float], list[float]]:
    p = list(zip(*points))
    px = p[0]
    py = p[1]
    f = [inv_linear_by_points(px[i], py[i], px[i + 1], py[i + 1]) for i in range(3)]
    def func(y: float) -> list[float]:
        res = [fi(y) for fi in f]
        res = [v for v in res if v is not None]
        return res
    return func


def main(temp_json: str, rule_json: str, map_temp_rule: str, temp: float) -> float:
    temp_data = json.loads(temp_json)
    temp_data_norm = {v["id"]:func_by_points(v["points"]) for v in temp_data["температура"]}
    temp_data_values = {k:v(temp) for k,v in temp_data_norm.items()}

    rule_data = json.loads(rule_json)
    rule_data_norm = {v["id"]:inv_func_by_points(v["points"]) for v in rule_data["температура"]}

    map_temp_rule_data = json.loads(map_temp_rule)
    map_temp_rule_norm = {v[0]:v[1] for v in map_temp_rule_data}

    loc_max = [rule_data_norm[map_temp_rule_norm[name]](val) for name, val in temp_data_values.items()]
    loc_max = [min(s) for s in loc_max]
    loc_max = [s for s in loc_max if s > 0]

    return min(loc_max)

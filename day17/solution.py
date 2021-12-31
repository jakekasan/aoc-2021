from pathlib import Path
from typing import Set, Tuple

def real_data():
    with Path("./input.txt").open() as f:
        return f.read().strip("\n")

def test_data():
    return "target area: x=20..30, y=-10..-5"

def _parse_range(range_str: str) -> Tuple[int, int]:
    lower, upper = range_str.split("..")
    return int(lower), int(upper)

def _parse_instructions(raw: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    x_range, y_range = raw.lstrip("target area: ").split(", ")

    return _parse_range(x_range.lstrip("x=")), _parse_range(y_range.lstrip("y="))

Vec = Tuple[int, int]
def _is_between(a, b, c) -> bool:
    _min = min([b, c])
    _max = max([b, c])
    res = _min <= a <= _max
    # print(f"({_min} <= {a} <= {_max}) = {res}")
    return res

def does_it_reach(velocity: Vec, x_range: Vec, y_range: Vec) -> bool:
    cur_x, cur_y = (0, 0)
    v_x, v_y = velocity
    while (cur_x <= max(x_range)) and (cur_y >= (min(y_range))):
        if _is_between(cur_x, *x_range) and _is_between(cur_y, *y_range):
            return True
        cur_x = cur_x + v_x
        cur_y = cur_y + v_y
        if v_x != 0:
            v_x = v_x - 1 if v_x > 0 else v_x + 1
        v_y -= 1
    return False

def _get_max_height(x: int, y: int) -> int:
    last = -1
    cur_x, cur_y = (0, 0)
    while last < cur_y:
        last = cur_y
        cur_x += x
        cur_y += y
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
        y -= 1

    return last

def part1(data: str):
    x_range, y_range = _parse_instructions(data)

    max_height = -1
    max_height_dir = (0, 0)
    for x in range(200):
        for y in range(250):
            res = does_it_reach((x, y), x_range, y_range)
            if res:
                this_height = _get_max_height(x, y)
                if this_height > max_height:
                    max_height = this_height
                    max_height_dir = (x, y)
    
    print(f"{max_height = }, {max_height_dir = }")

def part2(data: str):
    x_range, y_range = _parse_instructions(data)

    velocities: Set[Vec] = set()
    for x in range(750):
        for y in range(-150, 400):
            res = does_it_reach((x, y), x_range, y_range)
            if res:
                velocities.add((x, y))
    
    print(f"{len(velocities) = }")

part1(real_data())

part2(real_data())

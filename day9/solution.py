from functools import reduce
import operator
from pathlib import Path
from typing import Generator, Iterable, List, Set, Tuple


def test_data() -> List[List[int]]:
    raw = """2199943210
3987894921
9856789892
8767896789
9899965678"""
    res = [list(map(int, list(row))) for row in raw.split("\n") if row]
    # print(res)
    return res

def real_data() -> List[List[str]]:
    with Path("./input.txt").open() as f:
        return [list(map(int, list(row))) for row in f.read().split("\n")] # type: ignore

def get_surroundings(x, y, data: List[List[int]]) -> List[int]:
    xs = [-1, 0, 1]
    ys = [-1, 0, 1]
    res = []
    for yd in ys:
        for xd in xs:
            xi = x + xd
            yi = y + yd
            if (xi < 0 or
                yi < 0 or
                abs(yd) == abs(xd) or
                not yi < len(data) or
                not xi < len(data[yi])):
                continue
            res.append(data[yi][xi])
    return res

def _get_surrounding_coords(x, y, data) -> Set[Tuple[int, int]]:
    xs = [-1, 0, 1]
    ys = [-1, 0, 1]
    res = set()
    for yd in ys:
        for xd in xs:
            xi = x + xd
            yi = y + yd
            if (xi < 0 or
                yi < 0 or
                abs(yd) == abs(xd) or
                not yi < len(data) or
                not xi < len(data[yi])):
                continue
            res.add((yi, xi))
    return res

def print_coords(coords: Set[Tuple[int, int]], data) -> None:
    print("\n========\n")
    for y in range(len(data)):
        for x in range(len(data[y])):
            print(f"{data[y][x] if (y,x) in coords else ' '}", end="")
        print("")
    print("\n========\n")

def get_basin(x: int, y: int, data: List[List[int]]) -> Set[Tuple[int, int]]:
    start = data[y][x]
    to_explore = {(_y, _x) for _y, _x in _get_surrounding_coords(x, y, data) if start < data[_y][_x] < 9}
    basin = {(y, x)} | to_explore
    while to_explore:
        new_to_explore: Set[Tuple[int, int]] = set()
        for new_point in to_explore:
            _y, _x = new_point
            value = data[_y][_x]
            surroundings = _get_surrounding_coords(_x, _y, data)
            for s in surroundings:
                s_y, s_x = s
                if s in basin:
                    continue
                if value < data[s_y][s_x] < 9:
                    basin.add(s)
                    new_to_explore.add(s)
        to_explore = new_to_explore

    return basin

def part1():
    data = real_data()
    points = []
    for y, lst in enumerate(data):
        for x, value in enumerate(lst):
            surroundings = get_surroundings(x, y, data)
            if all(value < s_value for s_value in surroundings):
                points.append(value)

    return sum(1 + p for p in points)

def part2():
    data = real_data()
    basins = []
    for y, lst in enumerate(data):
        for x, d in enumerate(lst):
            basin = get_basin(x, y, data)
            # print_coords(basin, data)
            basins.append(basin)

    three_largest = sorted(basins, key=len, reverse=True)[:3]

    return reduce(operator.mul, map(len, three_largest))


print(f"{part1() = }")

print(f"{part2() = }")
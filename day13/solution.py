from itertools import zip_longest
from pathlib import Path
from typing import List, Optional, Set, Tuple

Grid = List[List[bool]]
Fold = Tuple[Optional[int], Optional[int]]

def _parse_raw(text: str) -> Tuple[Grid, List[Fold]]:
    grid_lines, fold_lines = text.split("\n\n")

    points: Set[Tuple[int, int]] = set()
    for line in grid_lines.split("\n"):
        x, y = line.split(",")
        points.add((int(x), int(y)))

    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)

    grid = [[(xi, yi) in points for xi in range(max_x + 1)] for yi in range(max_y + 1)]

    folds: List[Fold] = []
    for fold_line in fold_lines.split("\n"):
        axis, num = fold_line.lstrip("fold along ").split("=")

        if axis == "y":
            folds.append((None, int(num)))
        else:
            folds.append((int(num), None))

    return grid, folds

def test_data():
    raw = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    return _parse_raw(raw)

def real_data() -> Tuple[Grid, List[Fold]]:
    with Path("./input.txt").open() as f:
        return _parse_raw(f.read().strip("\n"))

def fold(grid: Grid, x: Optional[int] = None, y: Optional[int] = None) -> Grid:
    if x is not None and y is None:
        result = []
        for row in grid:
            left = row[:x]
            right = row[(x+1):]
            if not len(left) == len(right):
                left_right = [left, list(reversed(right))]
                [shorter_vert, longer_vert] = sorted(left_right, key=len)
                left_fold = ([False] * (len(longer_vert) - len(shorter_vert))) + shorter_vert
                right_fold = longer_vert
            else:
                left_fold = left
                right_fold = list(reversed(right))
            if not len(left_fold) == len(right_fold):
                raise Exception
            result.append([a or b for a, b in zip(left_fold, right_fold)])
        return result
    elif y is not None and x is None:
        bottom = grid[:y]
        top = grid[(y+1):]
        if not len(bottom) == len(top):
            top_bottom: List[List[List[bool]]] = [bottom, list(reversed(top))]
            [shorter, longer] = sorted(top_bottom, key=len)
            bottom_fold: List[List[bool]] = longer
            top_fold = [[False] * len(longer[0])] * (len(longer) - len(shorter)) + shorter
        else:
            bottom_fold = bottom
            top_fold = list(reversed(top))

        result = []
        for bottom_row, top_row in zip(bottom_fold, top_fold):
            result.append([a or b for a, b in zip(bottom_row, top_row)])
        return result

    raise ValueError

def print_grid(grid: Grid) -> None:
    for line in grid:
        print("".join(" " if not x else "#" for x in line))

def part1(data: Tuple[Grid, List[Fold]]) -> int:
    grid, [first_fold, *_] = data

    x, y = first_fold

    result = fold(grid, x=x, y=y)

    return sum(sum(line) for line in result)

def part2(data: Tuple[Grid, List[Fold]]) -> str:
    grid, folds = data

    result = grid

    for _fold in folds:
        x, y = _fold

        result = fold(result, x=x, y=y)

    return "\n".join("".join(" " if not x else "#" for x in row) for row in result)


print(f"{part1(real_data()) = }")
print(f"part 2: \n{part2(real_data())}")

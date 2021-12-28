from collections import defaultdict
from math import inf as Infinity
from pathlib import Path
from typing import Callable, Dict, List, Set, Tuple

GridMap = Dict[Tuple[int, int], int]

def _parse_raw(raw: str) -> GridMap:
    points: GridMap = dict()
    for y, row in enumerate(raw.split("\n")):
        for x, value in enumerate(row):
            points[(x, y)] = int(value)

    return points

def test_data():
    raw = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

    return _parse_raw(raw)

def real_data() -> GridMap:
    with Path("./input.txt").open() as f:
        return _parse_raw(f.read().strip("\n"))

def _get_options(point: Tuple[int, int], max_x: int, max_y: int) -> List[Tuple[int, int]]:
    ds = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    options = []
    for dx, dy in ds:
        x, y = point
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_x > max_x or new_y < 0 or new_y > max_y:
            continue
        options.append((new_x, new_y))
    return options

Point = Tuple[int, int]
def make_get_neighbours(points: GridMap) -> Callable[[Point], List[Point]]:
    ds = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]

    max_x = max(x for x, _ in points.keys())
    max_y = max(y for _, y in points.keys())

    def get_neighbours(point: Point) -> List[Point]:
        x, y = point
        neighbours = []
        for dx, dy in ds:
            new_x = x + dx
            new_y = y + dy

            if not (0 <= new_x <= max_x) or not (0 <= new_y <= max_y):
                continue

            neighbours.append((new_x, new_y))

        return neighbours
    return get_neighbours

def reconstruct_path(came_from: Dict[Point, Point], current: Point) -> List[Point]:
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path = [current] + total_path
    return total_path

def increase_grid(grid: GridMap) -> GridMap:
    new_grid: GridMap = dict()

    max_x = max(x for x, _ in grid.keys()) + 1
    max_y = max(y for _, y in grid.keys()) + 1

    for xd in range(5):
        for yd in range(5):
            for point, risk in grid.items():
                x, y = point
                new_point = (x + (max_x * xd), y + (max_y * yd))
                new_risk = (risk + xd + yd)
                while new_risk > 9:
                    new_risk -= 9
                new_grid[new_point] = new_risk

    return new_grid

def a_star(start: Point,
           end: Point,
           d: Callable[[Point], int],
           get_neighbours: Callable[[Point], List[Point]]) -> List[Point]:
    open_set: Set[Point] = {start}
    came_from: Dict[Point, Point] = dict()
    g_scores: Dict[Point, float] = defaultdict(lambda: Infinity)
    f_scores: Dict[Point, float] = defaultdict(lambda: Infinity)

    def h(p: Point) -> float:
        return ((end[0] - p[0])**2 + (end[1] - p[0])**2)**0.5

    f_scores[start] = h(start)
    g_scores[start] = 0

    while open_set:
        
        current, *_ = sorted(open_set, key=lambda p: f_scores[p])
        if current == end:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        for neighbour in get_neighbours(current):
            
            score = g_scores[current] + d(neighbour)

            if score < g_scores[neighbour]:
                came_from[neighbour] = current
                g_scores[neighbour] = score
                f_scores[neighbour] = score + h(neighbour)
                if neighbour not in open_set:
                    open_set.add(neighbour)

    raise Exception

def part1(grid: GridMap):
    def d(p: Point) -> int:
        return grid[p]
    get_neighbours = make_get_neighbours(grid)

    max_x = max(x for x, _ in grid.keys())
    max_y = max(y for _, y in grid.keys())
    start = (0, 0)
    end = (max_x, max_y)
    ideal_path = a_star(start, end, d=d, get_neighbours=get_neighbours)
    return sum(grid[p] if p != start else 0 for p in ideal_path)

def part2(grid: GridMap):
    new_grid = increase_grid(grid)
    return part1(new_grid)

def print_grid(grid: GridMap):
    max_x = max(x for x, _ in grid.keys())
    max_y = max(y for _, y in grid.keys())

    for y in range(max_y + 1):
        print("".join(str(grid[(x, y)]) for x in range(max_x + 1)))

print(f"{part1(real_data()) = }, {part2(real_data()) = }")

from pathlib import Path
from typing import Counter, List, Optional, Tuple


def test_data() -> List[List[int]]:
    raw = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    return [list(map(int, line)) for line in raw.split("\n")] # type: ignore

def real_data() -> List[List[int]]:
    with Path("./input.txt").open() as f:
        return [
            list(map(int, row)) for row in f.read().strip("\n").split("\n")
        ]

def test_data2() -> List[List[int]]:
    raw = """11111
19991
19191
19991
11111"""

    return [list(map(int, line)) for line in raw.split("\n")]

def get_neighbours(x: int, y: int, board: List[List[int]]) -> List[Tuple[int, int]]:
    ranges = [-1, 0, 1]
    neighbours: List[Tuple[int, int]] = []
    max_y = len(board) - 1
    max_x = len(board[0]) - 1
    for yd in ranges:
        for xd in ranges:
            if (yd, xd) == (0, 0):
                continue

            new_x = x + xd
            new_y = y + yd
            if new_x > max_x or new_y > max_y or new_x < 0 or new_y < 0:
                continue

            neighbours.append((new_x, new_y))
    return neighbours

def print_board(board: List[List[int]]):
    for row in board:
        row_string = "".join(str(num) if num > 0 else "*" for num in row)
        print(row_string)

def part1(data: List[List[int]], steps: int = 5) -> int:
    flashes = 0
    board = data

    print("Starting board:")
    print_board(board)
    for step_no in range(steps):
        increased_board: List[List[int]] = [[old_value + 1 for old_value in row] for row in board]

        queue: List[Tuple[int, int]] = []

        # start with 9s
        for y, row in enumerate(increased_board):
            for x, value in enumerate(row):
                if value <= 9:
                    continue
                flashes += 1
                neighbours = get_neighbours(x, y, increased_board)

                queue.extend(neighbours)

        new_board = [[value for value in row] for row in increased_board]

        while queue:
            counter = Counter(queue)
            [((x, y), count)] = counter.most_common(1)
            queue = [(_x, _y) for _x, _y in queue if not (x, y) == (_x, _y)]
            current_value = new_board[y][x]

            if current_value > 9:
                continue

            new_value = current_value + count

            if new_value > 9:

                flashes += 1

                neighbours = [
                    (_x, _y)
                    for (_x, _y) in get_neighbours(x, y, new_board)
                    if new_board[_y][_x] < 10
                ]

                queue.extend(neighbours)
            
            new_board[y][x] = new_value

        board = [[value if value < 10 else 0 for value in row] for row in new_board]
    return flashes

def part2(data: List[List[int]]) -> int:
    board = data

    print("Starting board:")
    print_board(board)
    run = 1
    while True:
        flashes = 0
        increased_board: List[List[int]] = [[old_value + 1 for old_value in row] for row in board]

        queue: List[Tuple[int, int]] = []

        # start with 9s
        for y, row in enumerate(increased_board):
            for x, value in enumerate(row):
                if value <= 9:
                    continue
                flashes += 1
                neighbours = get_neighbours(x, y, increased_board)

                queue.extend(neighbours)

        new_board = [[value for value in row] for row in increased_board]

        while queue:
            counter = Counter(queue)
            [((x, y), count)] = counter.most_common(1)
            queue = [(_x, _y) for _x, _y in queue if not (x, y) == (_x, _y)]
            current_value = new_board[y][x]

            if current_value > 9:
                continue

            new_value = current_value + count

            if new_value > 9:

                flashes += 1

                neighbours = [
                    (_x, _y)
                    for (_x, _y) in get_neighbours(x, y, new_board)
                    if new_board[_y][_x] < 10
                ]

                queue.extend(neighbours)
            
            new_board[y][x] = new_value

        board = [[value if value < 10 else 0 for value in row] for row in new_board]

        if flashes == len([item for row in board for item in row]):
            return run

        run += 1

print(f"{part1(real_data(), steps=100) = }")
print(f"{part2(real_data()) = }")

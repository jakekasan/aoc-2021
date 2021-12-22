from typing import List, Optional, Tuple


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

def get_neighbours(x: int, y: int, board: List[List[int]]) -> List[Tuple[int, int]]:
    ranges = [-1, 0, 1]
    neighbours: List[Tuple[int, int]] = []
    max_y = len(board) - 1
    max_x = len(board[0]) - 1
    # print(f"{max_x = }, {max_y = }")
    for yd in ranges:
        for xd in ranges:
            if (yd, xd) == (0, 0):
                continue
            new_x = x + xd
            new_y = y + yd
            if new_x > max_x or new_y > max_y:
                continue
            neighbours.append((new_x, new_y))
    # print(neighbours)
    return neighbours

def print_board(board: List[List[int]]):
    for row in board:
        row_string = "".join(str(num) if num > 0 else "*" for num in row)
        print(row_string)

def part1(data: List[List[int]], steps: int = 5):
    flashes = 0
    board = data
    for step_no in range(steps):
        increases: List[List[int]] = [[1 for _ in row] for row in board]
        for num in range(9, -1, -1):
            for y, row in enumerate(board):
                for x, item in enumerate(row):
                    if item != num:
                        continue

                    neighbours = get_neighbours(x, y, board)

                    for _x, _y in neighbours:
                        if num + increases[y][x] > 9:
                            increases[_y][_x] += 1

        new_board: List[List[int]] = [[0 for _ in row] for row in board]
        for y, row in enumerate(board):
            for x, item in enumerate(row):
                new_item = item + increases[y][x]
                if new_item > 9:
                    flashes += 1
                    new_item = 0
                new_board[y][x] = new_item

        print(f"After {step_no + 1} steps, {flashes} flashes")
        print_board(new_board)

        board = new_board

    return flashes
                

print(f"{part1(test_data(), steps=10) = }")

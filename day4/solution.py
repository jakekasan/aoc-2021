from pathlib import Path
from textwrap import dedent
from typing import Iterable, List, Set, Tuple

def test_data() -> str:
    return dedent("""
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7
    """).strip("\n")

def real_data() -> str:
    with Path("./input.txt").open() as f:
        return f.read()

def split(data: str) -> Tuple[List[int], List[List[List[int]]]]:
    raw_numbers, *raw_boards = data.split("\n\n")

    boards = []

    for raw_board in raw_boards:
        board = []
        for raw_row in raw_board.split("\n"):
            if not raw_row:
                continue
            board.append(list(map(int, raw_row.split())))
        boards.append(board)

    return list(map(int, raw_numbers.split(","))), boards

numbers, boards = split(real_data())

def part1(numbers: Iterable[int], boards: List[List[List[int]]]) -> int:
    seen: Set[int] = set()
    for num in numbers:
        seen.add(num)
        for board in boards:
            rows_n_cols: List[Iterable[Iterable[int]]] = [board, zip(*board)]
            for nums in [x for b in rows_n_cols for x in b]:
                if all(x in seen for x in nums):
                    print("Winner:", nums)
                    unmarked = list(x for row in board for x in row if x not in seen)
                    return sum(unmarked) * num

    raise Exception

def part2(numbers: Iterable[int], boards: List[List[List[int]]], seen: Set[int] = None) -> int:
    if seen is None:
        seen = set()
    n = len(boards)
    for num in numbers:
        seen.add(num)
        for board in boards:
            rows_n_cols: List[Iterable[Iterable[int]]] = [board, zip(*board)]
            for nums in [x for b in rows_n_cols for x in b]:
                if all(x in seen for x in nums):
                    other_boards = [b for b in boards if not b is board]
                    if not other_boards:    
                        print("Winner:", nums)
                        unmarked = list(x for row in board for x in row if x not in seen)
                        print("Num:", num)
                        print("Unmarked", sum(unmarked))
                        return sum(unmarked) * num
                    else:
                        return part2(numbers, other_boards, seen=seen)

    raise Exception

print(part2(numbers, boards))

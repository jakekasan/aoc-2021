from collections import Counter
from math import factorial
from pathlib import Path
from typing import List, Tuple


def test_data() -> List[int]:
    return [16,1,2,0,4,2,7,1,2,14]

def real_data() -> List[int]:
    with Path("./input.txt").open() as f:
        data = f.read().strip("\n")
        return list(map(int, data.split(",")))

def part1(fuel: List[int]) -> int:
    least = min(fuel)
    most = max(fuel)

    arr: List[Tuple[int, int]] = []
    for target in range(least, most + 1):
        arr.append((target, sum(abs(target - f) for f in fuel)))

    least_targets = sorted(arr, key=lambda target: target[1])[:10]

    return min((b for _, b in arr))

def part2(fuel: List[int]) -> int:
    least = min(fuel)
    most = max(fuel)

    arr: List[Tuple[int, int]] = []
    for target in range(least, most + 1):
        arr.append((target, sum(sum(range(abs(target - f) + 1)) for f in fuel)))

    least_targets = sorted(arr, key=lambda target: target[1])[:10]

    print(least_targets)
    return min((b for _, b in arr))

print(f"{part1(test_data()) = }, {part1(real_data()) = }")
print(f"{part2(test_data()) = }, {part2(real_data()) = }")

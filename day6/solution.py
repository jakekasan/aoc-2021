from collections import defaultdict
from pathlib import Path
from typing import Dict, List


def test_data() -> List[int]:
    return [3,4,3,1,2]

def real_data() -> List[int]:
    with Path("./input.txt").open() as f:
        return list(int(x) for x in f.read().split(","))

def advance(fish: List[int], days: int = 8, _print: bool = False) -> List[int]:
    if days < 1:
        return fish
    current_state = fish
    if _print:
        print("Initial state:", ",".join(map(str, current_state)))
    for _ in range(days):
        new_state = []
        for f in current_state:
            if f == 0:
                new_state.extend([6, 8])
            else:
                new_state.append(f - 1)
        current_state = new_state
        if _print:
            print(f"After {_ + 1} days:", len(current_state))
    
    return current_state

def part1(fish: List[int]) -> int:
    return len(advance(fish, days=80))

def part2(fish: List[int]) -> int:
    current_cycle: Dict[int, int] = defaultdict(int)
    
    for fishie in set(fish):
        current_cycle[fishie] = fish.count(fishie)

    for _ in range(256):
        next_cycle: Dict[int, int] = defaultdict(int)

        for fish_life in range(1, 9):
            next_cycle[fish_life - 1] += current_cycle[fish_life]

        next_cycle[8] += current_cycle[0]
        next_cycle[6] += current_cycle[0]

        current_cycle = next_cycle
    
    return sum(current_cycle.values())

print(f"{part1(real_data()) = }, {part2(real_data()) = }")
from io import StringIO
from pathlib import Path
from typing import Generator, Iterable, TextIO, Tuple

data_path = Path("./input.txt")

def get_inputs(io: TextIO = None) -> Generator[Tuple[str, int], None, None]:
    if io is None:
        io = data_path.open()
    for line in io.readlines():
        action, number = line.split(" ")
        yield action, int(number)

def final_position(start: Tuple[int, int], actions: Iterable[Tuple[str, int]]):
    pos, dep = start
    for action, amount in actions:
        if action == "forward":
            pos += amount
        if action == "down":
            dep += amount
        if action == "up":
            dep -= amount
    return pos, dep

test_input = StringIO("""forward 5
down 5
forward 8
up 3
down 8
forward 2""")

start = (0, 0)
actions = get_inputs()

pos, dep = final_position(start, actions)

print("Part 1:", pos * dep)

def final_position_2(start: Tuple[int, int], actions: Iterable[Tuple[str, int]]):
    pos, dep = start
    aim = 0
    for action, amount in actions:
        if action == "forward":
            pos += amount
            dep += aim * amount
        if action == "down":
            aim += amount
        if action == "up":
            aim -= amount
    return pos, dep

test_input = StringIO("""forward 5
down 5
forward 8
up 3
down 8
forward 2""")

start = (0, 0)
actions = get_inputs()

pos, dep = final_position_2(start, actions)

print("Part 2:", pos * dep)
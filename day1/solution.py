from pathlib import Path
from typing import Generator, Iterable, List, Tuple

data_path = Path("./input.txt")

def read_as_ints(path: Path) -> Generator[int, None, None]:
    with path.open() as p:
        for line in p.readlines():
            yield int(line)

def take_n(arr: Iterable[int], n: int = 2) -> Generator[List[int], None, None]:
    it = iter(arr)
    try:
        result: List[int] = [next(it) for _ in range(n)]
        while True:
            yield result
            result = result[1:] + [next(it)]
    except StopIteration:
        return

int_gen = read_as_ints(data_path)

# int_gen = iter([
#     199,
#     200,
#     208,
#     210,
#     200,
#     207,
#     240,
#     269,
#     260,
#     263,
# ])


print("Step 1:", sum(1 if a < b else 0 for a, b in take_n(read_as_ints(data_path), n=2)))

triplets: Iterable[int] = map(sum, take_n(read_as_ints(data_path), n=3))
print("Step 2:", sum(1 if a < b else 0 for a, b in take_n(triplets, n=2)))
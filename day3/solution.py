from collections import Counter
from pathlib import Path
from textwrap import dedent
from typing import Counter, Iterable, List

def test_data() -> List[str]:
    return dedent("""
            00100
            11110
            10110
            10111
            10101
            01111
            00111
            11100
            10000
            11001
            00010
            01010
""").strip("\n").split("\n")

def real_data() -> List[str]:
    with Path("./input.txt").open() as f:
        return [
            line.strip("\n")
            for line in f.readlines()
            if line not in ("", "\n")
        ]

def gen_bins():
    curr = 1
    while True:
        yield curr
        curr <<= 1

test = "01001"

def unbinary(string: str) -> int:
    return sum(int(s) * b for s,b in zip(reversed(string), gen_bins()))

def most_common(arr: Iterable[str]) -> str:
    c = Counter(arr)
    (value, _), *_ = c.most_common()
    # print("Most common:", value)
    return value

def least_common(arr: Iterable[str]) -> str:
    c = Counter(arr)
    *_, (value, _) = c.most_common()
    # print("Least common:", value)
    return value

def part2(arr: Iterable[str], most=True) -> str:
    valid = list(arr)

    idx = 0
    while len(valid) > 1:
        # print("Index:", idx)
        # print("Valid:", valid)
        c = Counter(map(lambda x: x[idx], valid))

        counted = c.most_common()

        # print(counted)
        [(most_value, most_count), (least_value, least_count)] = counted

        ints = list(map(int, [least_value, most_value]))
        if least_count == most_count:
            value = str(max(ints) if most else min(ints))
        else:
            value = most_value if most else least_value

        # print(f"{'Most' if most else 'Least'} common value is {value}")
        # print("Old length:", len(valid))
        valid = [v for v in valid if v[idx] == value]
        # print("New length:", len(valid))

        idx += 1

    [result] = valid

    # print(f"{'Most' if most else 'Least'} common result is {result}")

    return result

arr = real_data()

gamma = unbinary("".join(map(most_common, zip(*arr))))
epsilon = unbinary("".join(map(least_common, zip(*arr))))

print("Part 1")
print("Gamma:", gamma)
print("Epsilon:", epsilon)
print("Answer:", gamma * epsilon)

oxygen = unbinary(part2(arr, most=True))
co2 = unbinary(part2(arr, most=False))
print("Part 2")
print("Oxygen:", oxygen)
print("CO2:", co2)
print("Answer:", oxygen * co2)

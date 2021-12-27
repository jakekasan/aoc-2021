from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Dict, Generator, List, Tuple


def _parse_raw(text: str) -> Tuple[str, Dict[str, str]]:
    template, raw_mappings = text.split("\n\n")

    mappings: Dict[str, str] = dict()

    for line in raw_mappings.split("\n"):
        key, value = line.split(" -> ")
        mappings[key] = value

    return template, mappings

def real_data():
    with Path("./input.txt").open() as f:
        return _parse_raw(f.read().strip("\n"))

def test_data():
    raw = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
    return _parse_raw(raw)

def pair_gen(text: str) -> Generator[str, None, None]:
    for i in range(len(text)):
        subset = text[i:i+2]
        if len(subset) != 2:
            return
        yield subset

def make_expand(mappings: Dict[str, str], steps: int = 5) -> Callable[[str], Generator[str, None, None]]:

    def expand(pair: str, steps: int = steps) -> Generator[str, None, None]:
        for _ in range(steps):
            yield from expand(f"{pair[0]}{mappings[pair]}", steps=steps-1)
        yield f"{mappings[pair]}{pair[-1]}"

    return expand

def part1(data: Tuple[str, Dict[str, str]], steps: int = 10) -> int:
    text, mappings = data
    result = text
    for step in range(steps):
        # print(f"Step {step + 1}")
        new_result = f"{result[0]}"
        for pair in pair_gen(result):
            if pair in mappings:
                new_result += f"{mappings[pair]}{pair[-1]}"
        result = new_result

    c = Counter(result)
    (_, most_common_count), *_, (_, least_common_count) = c.most_common()

    return most_common_count - least_common_count

def part2(data: Tuple[str, Dict[str, str]], steps: int = 10) -> int:
    text, mappings = data
    counts: Dict[str, int] = defaultdict(int)
    pairs = list(pair_gen(text))
    for p in pairs:
        counts[p] += 1
    for _ in range(steps):
        new_counts: Dict[str, int] = defaultdict(int)
        for p, count in counts.items():
            v = mappings[p]
            new_counts[p[0] + v] += count
            new_counts[v + p[1]] += count
        counts = new_counts

    char_counts: Dict[str, int] = defaultdict(int)
    for key, value in counts.items():
        _, second = key[0], key[1]
        char_counts[second] += value

    char_counts[text[0]] += 1
    return max(char_counts.values()) - min(char_counts.values())

print(f"{part1(real_data()) = }, {part2(real_data(), steps=40) = }")

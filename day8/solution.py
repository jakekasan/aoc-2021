from collections import defaultdict
from pathlib import Path
from typing import Counter, Dict, List, Set, Tuple


def test_data() -> Tuple[List[str], List[str]]:
    raw_str = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf"""

    patterns, output_values = raw_str.split("|")

    return patterns.strip("\n").split(" "), output_values.strip("\n").split(" ")

def test_data2() -> List[Tuple[List[str], List[str]]]:
    raw = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

    lines = []

    for line in raw.split("\n"):
        left, right = line.split(" | ")

        lines.append((left.split(" "), right.split(" ")))

    return lines

def real_data() -> List[Tuple[List[str], List[str]]]:
    with Path("./input.txt").open() as f:
        raw = f.read()

    lines = []

    for line in raw.split("\n"):
        if not line:
            continue
        left, right = line.split(" | ")

        lines.append((left.split(" "), right.split(" ")))

    return lines

signal_mappings: Dict[int, Set[str]] = {
    0: set("abcefg"),
    1: set("cf"), # single
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"), # single
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"), # single
    8: set("abcdefg"), # single
    9: set("abcdfg")
}

def get_parser(line: List[str]) -> Dict[str, str]:
    by_len: Dict[int, List[Set[str]]] = defaultdict(list)
    for item in line:
        by_len[len(item)].append(set(item))
    one = by_len[2][0]
    seven = by_len[3][0]
    four = by_len[4][0]
    a, *_ = seven ^ one
    c_or_f = seven & one
    b_or_d = four ^ c_or_f
    five, *_ = [s for s in by_len[5] if not any(_ not in s for _ in b_or_d)]
    nine, *_ = [s for s in by_len[6] if ((c_or_f | b_or_d) & s == (c_or_f | b_or_d))]
    g, *_ = nine ^ ({a} | c_or_f | b_or_d)
    c, *_ = five ^ (c_or_f | b_or_d | {a} | {g})
    f, *_ = {c} ^ c_or_f
    eight = by_len[7][0]
    e, *_ = nine ^ eight
    six, *_ = [s for s in by_len[6] if s != nine and (b_or_d & s == b_or_d)]
    zero, *_ = [s for s in by_len[6] if s not in (six, nine)]
    two, *_ = [s for s in by_len[5] if s != five and (f not in s)]
    d, *_ = {a, c, e, g} ^ two
    b, *_  = {d} ^ b_or_d
    
    return {
        a: "a",
        b: "b",
        c: "c",
        d: "d",
        e: "e",
        f: "f",
        g: "g"
    }

def parse_line(line: List[str], parser: Dict[str, str]) -> int:
    reversed_signal_mappings = {"".join(sorted(signal)): str(number) for number, signal in signal_mappings.items()}
    results: List[str] = []
    for item in line:
        parsed_item = "".join(sorted(parser[i] for i in item))
        results.append(reversed_signal_mappings[parsed_item])
    return int("".join(results))

def part1():
    lines = real_data()

    output_lines = [b for _, b in lines]

    targets = {1,4,7,8}

    count = 0

    for line in output_lines:
        line_mappings: Dict[int, List[Set[str]]] = defaultdict(list)
        # print(line)
        for item in line:
            for k, v in signal_mappings.items():
                si = set(item)
                if len(si) == len(v):
                    # print(f"Possible {k}: '{item}'")
                    line_mappings[k].append(si)

        for k, v in line_mappings.items():
            if k in targets:
                count += len(v)

    return count


def part2():
    lines = real_data()

    total = 0
    for input_line, output_line in lines:
        parser = get_parser(input_line + output_line)
        result = parse_line(output_line, parser)
        total += result

    return total

print(f"{part1() = }, {part2() = }")
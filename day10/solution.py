from pathlib import Path
from typing import List


def test_data() -> List[str]:
    raw = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
    return raw.split("\n")

def real_data() -> List[str]:
    with Path("./input.txt").open() as f:
        return f.read().split("\n")

pairs = {
    "{": "}",
    "[": "]",
    "<": ">",
    "(": ")"
}

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

scores2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def part1():
    data = real_data()

    total_score = 0

    for line in data:
        opened: List[str] = list()
        for char in line:
            if char in pairs:
                opened.append(char)
            elif char in pairs.values():
                expected = pairs[opened[-1]]
                if char != expected:
                    total_score += scores[char]
                    break
                else:
                    *opened, _ = opened

    return total_score

def part2():
    data = real_data()

    line_scores = []

    for line in data:
        opened: List[str] = list()
        for char in line:
            if char in pairs:
                opened.append(char)
            elif char in pairs.values():
                expected = pairs[opened[-1]]
                if char != expected:
                    break
                else:
                    *opened, _ = opened
        else:
            if opened:
                total_score = 0
                required = [pairs[item] for item in reversed(opened)]

                for req in required:
                    total_score *= 5
                    total_score += scores2[req]

                line_scores.append(total_score)

    line_scores = sorted(line_scores)
    if len(line_scores) % 2 == 0:
        middle = max(line_scores[len(line_scores) // 2:len(line_scores // 2) + 1])
    else:
        middle = line_scores[len(line_scores) // 2]
    return middle

print(f"{part1() = }, {part2() = }")
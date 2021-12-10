from collections import Counter
from pathlib import Path


raw = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def test_data():
    lines = []
    for raw_line in raw.split("\n"):
        start, end = raw_line.split(" -> ")
        lines.append((tuple(map(int, start.split(","))), tuple(map(int, end.split(",")))))
    return lines

def real_data():
    lines = []
    with Path("./input.txt").open() as f:
        for line in f.readlines():
            start, end = line.split(" -> ")
            lines.append((tuple(map(int, start.split(","))), tuple(map(int, end.split(",")))))
        return lines

def get_line_points(lines, diagonal=False):
    points = []
    for ((x1, y1), (x2, y2)) in lines:
        if not diagonal and not (x1 == x2 or y1 == y2):
            continue
        if y1 == y2:
            ys = [y1 for _ in range(abs(x1 - x2) + 1)]
        else:
            y_step = 1 if y1 < y2 else -1
            ys = range(y1, y2 + y_step, y_step)

        if x1 == x2:
            xs = [x1 for _ in range(abs(y1 - y2) + 1)]
        else:
            x_step = 1 if x1 < x2 else -1
            xs = range(x1, x2 + x_step, x_step)

        line_points = [(x, y) for x, y in zip(xs, ys)]
        points.extend(line_points)
    return points

def print_points(points):
    xs = [x for (x, y) in points]
    ys = [y for (x, y) in points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    c = Counter(points)
    for y in range(min_y, max_y + 1):
        print(" ".join(str(c.get((x, y), ".")) for x in range(min_x, max_x + 1)))


def get_overlaps(points):
    c = Counter(points)
    # print_points(points)
    return len([a for a, b in c.most_common() if b >= 2])

print("Part 1:", get_overlaps(get_line_points(real_data(), diagonal=False)))
print("Part 2:", get_overlaps(get_line_points(real_data(), diagonal=True)))

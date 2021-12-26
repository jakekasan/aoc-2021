from pathlib import Path
from typing import Callable, Counter, Iterable, List, Set, Tuple

def _parse_text(text: str) -> List[Tuple[str, str]]:
    return [tuple(line.split("-")) for line in text.split("\n")] # type: ignore

def test_data() -> List[Tuple[str, str]]:
    raw = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

    return _parse_text(raw)

# print(test_data())

def test_data2():
    raw = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    return _parse_text(raw)

def test_data3():
    raw = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

    return _parse_text(raw)

def real_data():
    with Path("./input.txt").open() as f:
        return _parse_text(f.read().strip("\n"))

def part1(links: List[Tuple[str, str]]):
    routes: Set[Iterable[str]] = set([("start",)])
    finished_routes = set()
    seen = set()

    while routes:
        new_routes: Set[Iterable[str]] = set()
        seen.update(routes)

        for path in routes:
            *rest_of_path, end = path

            matching_links = [link
                              for link in links
                              if end in link and not any(point.islower() and point in rest_of_path for point in link)]

            for new_link in matching_links:
                next_point = new_link[0] if new_link[0] != end else new_link[1]
                if next_point == "start":
                    continue

                new_route = (*rest_of_path, end, next_point)

                if next_point == "end":
                    finished_routes.add(new_route)

                else:
                    new_routes.add(new_route)

        routes = {r for r in new_routes if r not in seen}

    return len(finished_routes)

def _make_is_valid(path: Iterable[str]) -> Callable[[Tuple[str, str]], bool]:
    *_, end = path
    c = Counter(p for p in path if p.islower())
    def _is_valid(link: Tuple[str, str]) -> bool:
        if end not in link:
            return False
        
        new_point = link[0] if link[0] != end else link[1]

        if not new_point.islower():
            return True

        if new_point not in c:
            return True

        _c = Counter([count for _, count in c.most_common()])

        return _c.get(2, 0) < 1

    return _is_valid

def part2(links: List[Tuple[str, str]]):
    routes: Set[Iterable[str]] = set([("start",)])
    finished_routes = set()
    seen = set()

    while routes:
        new_routes: Set[Iterable[str]] = set()
        seen.update(routes)

        for path in routes:
            *rest_of_path, end = path

            _is_valid = _make_is_valid(path)

            matching_links = [link
                              for link in links
                              if _is_valid(link)]

            for new_link in matching_links:
                next_point = new_link[0] if new_link[0] != end else new_link[1]
                if next_point == "start":
                    continue

                new_route = (*rest_of_path, end, next_point)

                if next_point == "end":
                    finished_routes.add(new_route)

                else:
                    new_routes.add(new_route)
            
        routes = {r for r in new_routes if r not in seen}

    return len(finished_routes)

print(f"{part1(real_data()) = }, {part2(real_data()) = }")

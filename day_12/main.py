"""Advent of Code 2021 - Day 12

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Dict
from typing import List
from typing import Tuple

from collections import Counter
from collections import defaultdict


def read_input(filename: str) -> List[Tuple[str, str]]:
    with open(filename) as f:
        lines = f.readlines()
    result = []
    for line in lines:
        s, e = line.strip().split('-')
        result.append((s, e))

    return result


def map_list_to_dict(data: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    result = defaultdict(list)
    for start, end in data:
        if end != 'start':
            result[start].append(end)
        if start != 'start' and end != 'end':
            result[end].append(start)
    return result


def visit_cave(path: List[str], map_map: Dict[str, List[str]]):
    result = []
    current_cave = path[-1]
    if current_cave == 'end':
        result.append(path)
        return result

    for next_cave in map_map[current_cave]:
        if next_cave.islower() and next_cave in path:
            continue

        path_prim = path.copy()
        path_prim.append(next_cave)
        result.extend(visit_cave(path_prim, map_map))

    return result


def have_visited_small_cave_twice(path: List[str]) -> bool:
    for v, c in Counter(path).items():
        if v.islower() and c == 2:
            return True

    return False


def visit_cave_v2(path: List[str], map_map: Dict[str, List[str]]):
    result = []
    current_cave = path[-1]
    if current_cave == 'end':
        result.append(path)
        return result

    for next_cave in map_map[current_cave]:
        if (
            next_cave.islower()
            and next_cave in path
            and have_visited_small_cave_twice(path)
        ):
            continue

        path_prim = path.copy()
        path_prim.append(next_cave)
        result.extend(visit_cave_v2(path_prim, map_map))

    return result


def main():
    # Part 1
    data = read_input('input.txt')
    d = map_list_to_dict(data)

    paths = visit_cave(['start'], d)
    result = len(paths)
    print(result)
    assert result == 5333

    # Part 2
    paths_v2 = visit_cave_v2(['start'], d)
    result = len(paths_v2)
    print(result)
    assert result == 146553


if __name__ == '__main__':
    main()

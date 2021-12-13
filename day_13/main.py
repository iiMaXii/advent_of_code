"""Advent of Code 2021 - Day 13

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
from typing import List
from typing import Tuple


def read_input(filename: str) -> Tuple[List[Tuple[int, int]], List[Tuple[str, int]]]:
    with open(filename) as f:
        lines = f.readlines()

    coordinates = []
    folds = []
    fold_section = False
    for line in lines:
        line = line.strip()
        if not line:
            fold_section = True
            continue

        if not fold_section:
            x, y = line.split(',')
            coordinates.append((int(x), int(y)))
        else:
            assert line.startswith('fold along ')
            line = line[len('fold along ') :]
            axis, value = line.split('=')
            folds.append((axis, int(value)))

    return coordinates, folds


def get_dimensions(coordinates: List[Tuple[int, int]]) -> Tuple[int, int]:
    max_x = 0
    max_y = 0
    for x, y in coordinates:
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    return max_x + 1, max_y + 1


def coordinates_to_map_str(coordinates: List[Tuple[int, int]]) -> str:
    width, height = get_dimensions(coordinates)

    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in coordinates:
                row.append('#')
            else:
                row.append('.')
        lines.append(''.join(row))
    return '\n'.join(lines)


def perform_fold(
    coordinates: List[Tuple[int, int]], axis: str, fold_value: int
) -> List[Tuple[int, int]]:
    result = set()
    for x, y in coordinates:
        value = x if axis == 'x' else y
        if value == fold_value:
            continue  # discard
        elif value < fold_value:
            result.add((x, y))
        else:
            value = fold_value - (value - fold_value)

            if axis == 'x':
                result.add((value, y))
            else:
                result.add((x, value))

    return list(result)


def main():
    # Part 1
    coordinates, folds = read_input('input.txt')

    new_list = None
    for axis, value in folds:
        new_list = perform_fold(coordinates, axis, value)
        break

    coordinate_count = len(new_list)

    print(coordinate_count)
    assert coordinate_count == 621

    # Part 2
    new_list = coordinates
    for axis, value in folds:
        new_list = perform_fold(new_list, axis, value)

    result = coordinates_to_map_str(new_list)
    print(result)

    # HKUJGAJZ
    assert (
        result == '#..#.#..#.#..#...##..##...##....##.####\n'
        '#..#.#.#..#..#....#.#..#.#..#....#....#\n'
        '####.##...#..#....#.#....#..#....#...#.\n'
        '#..#.#.#..#..#....#.#.##.####....#..#..\n'
        '#..#.#.#..#..#.#..#.#..#.#..#.#..#.#...\n'
        '#..#.#..#..##...##...###.#..#..##..####'
    )


if __name__ == '__main__':
    main()

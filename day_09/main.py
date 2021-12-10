"""Advent of Code 2021 - Day 9

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


def read_input(filename: str) -> List[List[int]]:
    with open(filename) as f:
        lines = f.readlines()
    result = []
    for line in lines:
        result.append([int(v) for v in line.strip()])

    return result


def get_adjacent_points(data, x, y) -> List[Tuple[int, int]]:
    adjacent_points = []

    if y != 0:
        adjacent_points.append((x, y - 1))

    if x != 0:
        adjacent_points.append((x - 1, y))

    if y != len(data) - 1:
        adjacent_points.append((x, y + 1))

    if x != len(data[0]) - 1:
        adjacent_points.append((x + 1, y))

    return adjacent_points


def get_adjacent_values(data, x, y) -> List[int]:
    return [data[y][x] for x, y in get_adjacent_points(data, x, y)]


def get_low_points(data: List[List[int]]) -> List[Tuple[int, int]]:
    low_points = []
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            adjacent_values = get_adjacent_values(data, x, y)

            min_value = min(value, *adjacent_values)
            if min_value == value and value not in adjacent_values:
                low_points.append((x, y))
    return low_points


def get_point_basin(
    data: List[List[int]], low_point: Tuple[int, int]
) -> List[Tuple[int, int]]:
    basin_points = [low_point]

    x, y = low_point
    low_point_value = data[y][x]
    adj_points = get_adjacent_points(data, x, y)
    for adj_x, adj_y in adj_points:
        if data[adj_y][adj_x] == 9:
            # "Locations of height 9 do not count as being in any basin"
            continue

        if data[adj_y][adj_x] > low_point_value:
            basin_points.extend(get_point_basin(data, (adj_x, adj_y)))

    return list(set(basin_points))


def main():
    # Part 1
    data = read_input('input.txt')

    low_points = get_low_points(data)
    low_points_values = [data[y][x] for x, y in low_points]

    risk_sum = sum([1 + p for p in low_points_values])
    print(risk_sum)
    assert risk_sum == 588

    # Part 2
    basins = [get_point_basin(data, low_point) for low_point in low_points]
    basins_sizes = [len(basin) for basin in basins]

    result = 1
    for v in sorted(basins_sizes, reverse=True)[:3]:
        result *= v

    print(result)
    assert result == 964712


if __name__ == '__main__':
    main()

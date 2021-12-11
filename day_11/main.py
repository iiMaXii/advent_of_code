"""Advent of Code 2021 - Day 11

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

from dataclasses import dataclass


@dataclass
class DumboOctopus:
    energy: int
    has_flashed: bool = False


def read_input(filename: str) -> List[List[DumboOctopus]]:
    with open(filename) as f:
        lines = f.readlines()
    result = []
    for line in lines:
        result.append([DumboOctopus(int(v)) for v in line.strip()])

    return result


def get_adjacent_coordinates(data, x, y) -> List[Tuple[int, int]]:
    adjacent_coordinates = []

    for y_offset in [-1, 0, 1]:
        for x_offset in [-1, 0, 1]:
            adj_x = x + x_offset
            adj_y = y + y_offset
            if 0 <= adj_x < len(data[0]) and 0 <= adj_y < len(data):
                adjacent_coordinates.append((adj_x, adj_y))

    return adjacent_coordinates


def perform_octopus_flash(data: List[List[DumboOctopus]], x: int, y: int):
    for x, y in get_adjacent_coordinates(data, x, y):
        oct = data[y][x]
        oct.energy += 1
        if not oct.has_flashed and oct.energy > 9:
            oct.has_flashed = True
            perform_octopus_flash(data, x, y)


def perform_cycle(data: List[List[DumboOctopus]]) -> int:
    for y, row in enumerate(data):
        for x, oct in enumerate(row):
            oct.energy += 1
            if not oct.has_flashed and oct.energy > 9:
                oct.has_flashed = True
                perform_octopus_flash(data, x, y)

    # Reset values higher than 9 and count flashes
    flash_count = 0
    for y, row in enumerate(data):
        for x, oct in enumerate(row):
            if oct.energy > 9:
                oct.energy = 0
                oct.has_flashed = False
                flash_count += 1
            else:
                assert not oct.has_flashed

    return flash_count


def main():
    # Part 1
    data = read_input('input.txt')

    flash_count = sum([perform_cycle(data) for _ in range(100)])
    print(flash_count)
    assert flash_count == 1644

    # Part 2
    data = read_input('input.txt')  # reset data
    total_oct_count = len(data) * len(data[0])

    step_count = 0
    while True:
        step_count += 1
        flash_count = perform_cycle(data)
        if flash_count == total_oct_count:
            print(step_count)
            break

    assert step_count == 229


if __name__ == '__main__':
    main()

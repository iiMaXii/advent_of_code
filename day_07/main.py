"""Advent of Code 2021 - Day 7

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

import statistics


def read_input(filename: str) -> List[int]:
    with open(filename) as f:
        lines = f.readlines()

    return [int(v) for v in lines[0].strip().split(',')]


def calculate_fuel_for_alignment_v1(
    horizontal_positions: List[int], alignment_level: int
) -> int:
    result = 0
    for p in horizontal_positions:
        result += abs(alignment_level - p)

    return result


def calculate_fuel_for_alignment_v2(
    horizontal_positions: List[int], alignment_level: int
) -> int:
    result = 0
    for p in horizontal_positions:
        result += sum(range(abs(alignment_level - p) + 1))

    return result


def main():
    # Part 1
    data = read_input('input.txt')
    fuel_required = calculate_fuel_for_alignment_v1(data, int(statistics.median(data)))
    print(f'fuel_required={fuel_required}')
    assert fuel_required == 348996

    # Part 2

    # Lets brute force this! (a faster would be to use binary search or start in the middle or something, but meh)
    actual_fuel_required = calculate_fuel_for_alignment_v2(data, 0)
    for hor_lvl in range(min(data), max(data) + 1):
        possible_fuel_requirement = calculate_fuel_for_alignment_v2(data, hor_lvl)
        if actual_fuel_required > possible_fuel_requirement:
            actual_fuel_required = possible_fuel_requirement

    print(f'actual_fuel_required={actual_fuel_required}')
    assert actual_fuel_required == 98231647


if __name__ == '__main__':
    main()

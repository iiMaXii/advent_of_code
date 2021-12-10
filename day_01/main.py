"""Advent of Code 2021 - Day 1

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


def read_input(filename: str) -> List[int]:
    with open(filename) as f:
        lines = f.readlines()

    return [int(v) for v in lines]


def calculate_sonar_differences(data: List[int]) -> List[int]:
    sonar_differences = []
    for previous_value, value in zip([None] + data, data):
        if previous_value is None:
            continue

        sonar_differences.append(value - previous_value)

    return sonar_differences


def calculate_increased_measurement_count(data: List[int]) -> int:
    data = calculate_sonar_differences(data)
    return sum([1 for d in data if d > 0])


def partition(input_data: List[int]) -> List[List[int]]:
    result = []
    for i in range(len(input_data) - 2):
        result.append(input_data[i : i + 3])

    return result


def main():
    # Part 1
    sonar_data = read_input('input.txt')

    result = calculate_increased_measurement_count(sonar_data)

    print(result)
    assert result == 1527

    # Part 2
    partitions = partition(sonar_data)
    partition_sums = [sum(p) for p in partitions]
    result = calculate_increased_measurement_count(partition_sums)
    print(result)
    assert result == 1575


if __name__ == '__main__':
    main()

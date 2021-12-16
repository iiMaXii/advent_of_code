"""Advent of Code 2021 - Day 14

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
from typing import Tuple

from collections import Counter
from collections import defaultdict


def read_input(filename: str) -> Tuple[str, Dict[str, str]]:
    with open(filename) as f:
        lines = f.readlines()

    polymer = lines[0].strip()

    result = {}
    for line in lines[2:]:
        a, b = line.strip().split(' -> ')
        result[a] = b

    return polymer, result


def perform_cycle(data, polymer_table: Dict[str, str]):
    result = []
    for index, part in enumerate(data):
        result.append(part)
        polymer = data[index : index + 2]
        if len(polymer) != 2:
            break
        result.append(polymer_table[polymer])
    return ''.join(result)


def data_to_dict(data: str) -> Dict[str, int]:
    result = defaultdict(int)
    for index, part in enumerate(data):
        polymer = data[index : index + 2]
        if len(polymer) != 2:
            break
        result[polymer] += 1
    return result


def perform_cycle_dict(data: Dict[str, int], polymer_table: Dict[str, str]):
    r = defaultdict(int)
    for polymer, count in data.items():
        a, b = polymer
        insertion_element = polymer_table[polymer]

        r[a + insertion_element] += count
        r[insertion_element + b] += count

    return r


def perform_count(data_dict: Dict[str, int]):
    r = defaultdict(int)
    for polymer, count in data_dict.items():
        a, _ = polymer
        r[a] += count
    return r


def main():
    # Part 1
    data, polymer_table = read_input('input.txt')

    new_polymer = data
    for i in range(10):
        new_polymer = perform_cycle(new_polymer, polymer_table)

    c = Counter(new_polymer)
    _, most_common_count = c.most_common()[0]
    _, least_common_count = c.most_common()[-1]

    result = most_common_count - least_common_count
    print(result)
    assert result == 3555

    # Part 2
    d = data_to_dict(data)
    r = d
    for i in range(40):
        r = perform_cycle_dict(r, polymer_table)

    count = perform_count(r)

    # The last element is not included in the count
    count[data[-1]] += 1

    c = Counter(count)
    _, most_common_count = c.most_common()[0]
    _, least_common_count = c.most_common()[-1]

    result = most_common_count - least_common_count
    print(result)
    assert result == 4439442043739


if __name__ == '__main__':
    main()

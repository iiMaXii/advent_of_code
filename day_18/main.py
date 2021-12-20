"""Advent of Code 2021 - Day 18

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
from typing import Optional
from typing import List

from dataclasses import dataclass
from math import ceil
from math import floor


def read_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


@dataclass
class _SnailfishValue:
    value: int
    nest_level: int


class SnailfishNumber:
    def __init__(self, expression: str = ''):
        self.flattened = self._parse_expression(expression)

    @staticmethod
    def _parse_expression(expression: str) -> List[_SnailfishValue]:
        flattened_value = []
        nest_count = 0
        for c in expression:
            if c == '[':
                nest_count += 1
            elif c == ']':
                nest_count -= 1
            elif c == ',':
                pass  # we assume that all numbers only have one digit
            else:
                flattened_value.append(_SnailfishValue(int(c), nest_count))
        return flattened_value

    @staticmethod
    def _explosivo(f: List[_SnailfishValue], index: int) -> None:
        left_left = f[index - 1] if index - 1 >= 0 else None
        left = f[index]
        right = f[index + 1]
        right_right = f[index + 2] if index + 2 < len(f) else None

        if left_left is not None:
            left_left.value += left.value

        if right_right is not None:
            right_right.value += right.value

        f.pop(index + 1)  # Remove right

        left.value = 0
        left.nest_level -= 1

    @staticmethod
    def _split(f: List[_SnailfishValue], index: int) -> None:
        value = f[index].value
        nest_level = f[index].nest_level
        right = f[index]

        right.value = ceil(value / 2)
        right.nest_level += 1
        left = _SnailfishValue(floor(value / 2), nest_level + 1)

        f.insert(index, left)

    @staticmethod
    def _find_pair_to_explode(f: List[_SnailfishValue]) -> Optional[int]:
        for index, (left, right) in enumerate(zip([_SnailfishValue(-1, -1)] + f, f)):
            if left.nest_level == right.nest_level and left.nest_level > 4:
                # Result is -1 since we added dummy pair (-1, -1) in the zip function
                return index - 1
        return None

    @staticmethod
    def _find_value_to_split(f: List[_SnailfishValue]) -> Optional[int]:
        for index, value in enumerate(f):
            if value.value >= 10:
                return index
        return None

    @staticmethod
    def _find_first_pair(flat) -> Optional[int]:
        for index, (a, b) in enumerate(zip([None] + flat, flat)):
            if a is None:
                continue

            if a.nest_level == b.nest_level:
                return index - 1

        return None

    def __add__(self, other: 'SnailfishNumber') -> 'SnailfishNumber':
        new_nbr = SnailfishNumber()
        new_nbr.flattened = self.flattened + other.flattened

        for v in new_nbr.flattened:
            v.nest_level += 1

        performed_operations_count = -1
        while performed_operations_count != 0:
            performed_operations_count = 0
            while True:
                index = self._find_pair_to_explode(new_nbr.flattened)
                if index is None:
                    break

                self._explosivo(new_nbr.flattened, index)
                performed_operations_count += 1

            index = self._find_value_to_split(new_nbr.flattened)
            if index is not None:
                self._split(new_nbr.flattened, index)
                performed_operations_count += 1

        return new_nbr

    def magnitude(self) -> int:
        flat_copy = self.flattened.copy()

        index = self._find_first_pair(flat_copy)
        while index is not None:
            flat_copy[index].value = (
                3 * flat_copy[index].value + 2 * flat_copy[index + 1].value
            )
            flat_copy[index].nest_level -= 1
            flat_copy.pop(index + 1)
            index = self._find_first_pair(flat_copy)

        assert len(flat_copy) == 1

        return flat_copy[0].value


def main():
    # Part 1
    terms = read_input('input.txt')

    s = sum([SnailfishNumber(term) for term in terms[1:]], SnailfishNumber(terms[0]))

    result = s.magnitude()
    print(result)
    assert result == 4457

    # Part 2
    magnitudes = []
    for t1 in terms:
        for t2 in terms:
            magnitudes.append((SnailfishNumber(t1) + SnailfishNumber(t2)).magnitude())

    result = max(magnitudes)
    print(result)
    assert result == 4784


if __name__ == '__main__':
    main()

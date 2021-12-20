"""Advent of Code 2021 - Day 20

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
from typing import Tuple
from typing import List


def read_input(filename: str) -> Tuple[List[int], List[List[int]]]:
    with open(filename) as f:
        lines = f.readlines()

    lookup_table = [1 if p == '#' else 0 for p in lines[0].strip()]
    picture = [[1 if p == '#' else 0 for p in line.strip()] for line in lines[2:]]

    return lookup_table, picture


def get_lookup_table_index(picture: List[List[int]], x: int, y: int, default: int = 0):
    width = len(picture[0])
    height = len(picture)

    digits = []

    for y_ in range(y - 1, y + 2):
        for x_ in range(x - 1, x + 2):
            if y_ < 0 or y_ >= height or x_ < 0 or x_ >= width:
                digits.append(str(default))
            else:
                digits.append(str(picture[y_][x_]))

    bin_number = ''.join(digits)
    return int(bin_number, 2)


def apply_image_enhancement_algorithm(
    picture: List[List[int]], lookup_table: List[int], default=0
) -> List[List[int]]:
    x_offset = 1
    y_offset = 1
    output = [
        [-1 for _ in range(len(picture[0]) + 2 * x_offset)]
        for _ in range(len(picture) + 2 * y_offset)
    ]

    for new_y, row in enumerate(output):
        for new_x, _ in enumerate(row):
            x = new_x - x_offset
            y = new_y - y_offset

            index = get_lookup_table_index(picture, x, y, default=default)
            output[new_y][new_x] = lookup_table[index]

    return output


def print_picture(picture: List[List[int]]):
    for row in picture:
        for value in row:
            print('#' if value else '.', end='')
        print()
    print()


def main():
    lookup_table, picture = read_input('input.txt')

    # If the following conditions are met we know that the "out of bounds" values toggle between 0 and 1 according to
    # the formula: i % 2, where i is the current pass count of the algorithm.
    assert lookup_table[0] == 1
    assert lookup_table[511] == 0

    r = picture
    for i in range(2):
        r = apply_image_enhancement_algorithm(
            r,
            lookup_table,
            default=i % 2,  # See comment for the lookup_table assertions above
        )

    result = sum([sum(v) for v in r])
    print(result)
    assert result == 5044

    r = picture
    for i in range(50):
        r = apply_image_enhancement_algorithm(
            r,
            lookup_table,
            default=i % 2,  # See comment for the lookup_table assertions above
        )

    result = sum([sum(v) for v in r])
    print(result)
    assert result == 18074


if __name__ == '__main__':
    main()

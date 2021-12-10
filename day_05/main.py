"""Advent of Code 2021 - Day 5

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
class VentPositionData:
    start_coord: Tuple[int, int]
    end_coord: Tuple[int, int]

    def is_diagonal(self) -> bool:
        x1, y1 = self.start_coord
        x2, y2 = self.end_coord

        return x1 != x2 and y1 != y2

    def get_all_coords(self) -> List[Tuple[int, int]]:
        x1, y1 = self.start_coord
        x2, y2 = self.end_coord

        result = []

        y_step = -1 if y1 > y2 else 1
        x_step = -1 if x1 > x2 else 1

        if self.is_diagonal():
            x, y = self.start_coord
            while True:
                result.append((x, y))
                x += x_step
                y += y_step

                if x == x2 and y == y2:
                    result.append((x2, y2))
                    break
        else:
            for y in range(y1, y2 + y_step, y_step):
                for x in range(x1, x2 + x_step, x_step):
                    result.append((x, y))
        return result


class VentDiagram:
    def __init__(self):
        self.diagram: List[List[int]] = []
        self.width = 0
        self.height = 0

    def _extend_diagram(self, coord: Tuple[int, int]):
        x, y = coord
        new_width = max(self.width, x + 1)
        new_height = max(self.height, y + 1)

        # Create new
        new_diagram = [[0 for _ in range(new_width)] for _ in range(new_height)]

        # Transfer data
        for y, row in enumerate(self.diagram):
            for x, count in enumerate(row):
                new_diagram[y][x] = count

        self.diagram = new_diagram
        self.width = new_width
        self.height = new_height

    def plot_coord(self, coord: Tuple[int, int]):
        x, y = coord
        if x >= self.width or y >= self.height:
            self._extend_diagram(coord)

        self.diagram[y][x] += 1

    def count_least_two_lines(self) -> int:
        result = 0
        for row in self.diagram:
            for count in row:
                if count >= 2:
                    result += 1

        return result


def read_input(filename: str) -> List[VentPositionData]:
    with open(filename) as f:
        lines = f.readlines()

    vents = []
    for line in lines:
        start, end = line.strip().split('->')
        x1, y1 = start.strip().split(',')
        x2, y2 = end.strip().split(',')
        vents.append(VentPositionData((int(x1), int(y1)), (int(x2), int(y2))))

    return vents


def main():
    # Part 1
    data = read_input('input.txt')

    d = VentDiagram()

    for line in data:
        if line.is_diagonal():
            continue

        for c in line.get_all_coords():
            d.plot_coord(c)

    result = d.count_least_two_lines()
    assert result == 6267
    print(result)

    # Part 2
    d = VentDiagram()

    for line in data:
        for c in line.get_all_coords():
            d.plot_coord(c)

    result = d.count_least_two_lines()
    assert result == 20196
    print(result)


if __name__ == '__main__':
    main()

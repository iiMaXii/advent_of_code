"""Advent of Code 2021 - Day 15

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

from dijkstra import Graph
from dijkstra import DijkstraSPF


def read_input(filename: str) -> List[List[int]]:
    with open(filename) as f:
        lines = f.readlines()

    result = []
    for line in lines:
        result.append([int(r) for r in line.strip()])

    return result


def get_adjacent_coordinates(data, x, y) -> List[Tuple[int, int]]:
    r = []
    for y_offset in [-1, 0, 1]:
        for x_offset in [-1, 0, 1]:
            if abs(y_offset) == abs(x_offset):
                continue

            adj_x = x + x_offset
            adj_y = y + y_offset
            if 0 <= adj_x < len(data[0]) and 0 <= adj_y < len(data):
                r.append((adj_x, adj_y))
    return r


def populate_graph(graph: Graph, data: List[List[int]]):
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            for x_adj, y_adj in get_adjacent_coordinates(data, x, y):
                graph.add_edge((x, y), (x_adj, y_adj), data[y_adj][x_adj])


def extend_graph(data: List[List[int]], dup_x: int, dup_y: int) -> List[List[int]]:
    width = len(data[0])
    height = len(data)

    result = [
        [data[y % height][x % width] for x in range(width * dup_x)]
        for y in range(height * dup_y)
    ]

    for y, row in enumerate(result):
        for x, value in enumerate(row):
            x_offset = x // width
            y_offset = y // height

            weight = (value + x_offset + y_offset - 1) % 9 + 1

            result[y][x] = weight

    return result


def print_path(data, path):
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if (x, y) in path:

                print(f'\033[94m{value}\033[0m', end='')
            else:
                print(f'{value}', end='')
        print()


def main():
    # Part 1
    data = read_input('input.txt')

    g = Graph()
    populate_graph(g, data)

    dijkstra = DijkstraSPF(g, (0, 0))

    end_position = (len(data[0]) - 1, len(data) - 1)
    result = dijkstra.get_distance(end_position)

    # print_path(data, dijkstra.get_path(end_position))
    print(result)
    assert result == 487

    # Part 2
    data_2 = extend_graph(data, 5, 5)

    g = Graph()
    populate_graph(g, data_2)

    dijkstra = DijkstraSPF(g, (0, 0))

    end_position_2 = (len(data_2[0]) - 1, len(data_2) - 1)
    result = dijkstra.get_distance(end_position_2)

    # print_path(data_2, dijkstra.get_path(end_position_2))
    print(result)
    assert result == 2821


if __name__ == '__main__':
    main()

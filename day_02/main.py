"""Advent of Code 2021 - Day 2

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
from enum import Enum
from enum import auto


@dataclass
class Location:
    horizontal: int = 0
    depth: int = 0

    # Part 2
    aim: int = 0


class Course(Enum):
    FORWARD = auto()
    DOWN = auto()
    UP = auto()


NavigationData = List[Tuple[Course, int]]


def read_input(file: str) -> NavigationData:
    result = []
    with open(file) as f:
        instructions = f.readlines()

    instructions = [i.split() for i in instructions]
    for course, value in instructions:
        result.append((Course[course.upper()], int(value)))

    return result


def navigate(location: Location, nav_data: NavigationData):
    for course, value in nav_data:
        if course is Course.FORWARD:
            location.horizontal += value
        elif course is Course.DOWN:
            location.depth += value
        elif course is Course.UP:
            location.depth -= value
        else:
            raise ValueError()


def navigate_v2(location: Location, nav_data: NavigationData):
    for course, value in nav_data:
        if course is Course.FORWARD:
            location.horizontal += value
            location.depth += location.aim * value
        elif course is Course.DOWN:
            location.aim += value
        elif course is Course.UP:
            location.aim -= value
        else:
            raise ValueError()


def main():
    # Part 1
    nav_data = read_input('input.txt')
    location = Location()
    navigate(location, nav_data)
    result = location.horizontal * location.depth
    print(result)
    assert result == 2187380

    # Part 2
    location = Location()
    navigate_v2(location, nav_data)
    result = location.horizontal * location.depth
    print(result)
    assert result == 2086357770


if __name__ == '__main__':
    main()

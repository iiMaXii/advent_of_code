"""Advent of Code 2021 - Day 17

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
from dataclasses import dataclass
import re


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Area:
    start: Point
    end: Point


@dataclass
class ProbeStatistics:
    hit_counter: int = 0
    max_altitude: int = 0


def read_input(filename: str) -> Area:
    with open(filename) as f:
        lines = f.readlines()

    line = lines[0]
    m = re.search(r'x=(-?\d+)..(-?\d+)', line)
    x1 = int(m.group(1))
    x2 = int(m.group(2))

    m = re.search(r'y=(-?\d+)..(-?\d+)', line)
    y1 = int(m.group(1))
    y2 = int(m.group(2))

    return Area(Point(x1, y1), Point(x2, y2))


def is_in_area(position: Point, area: Area) -> bool:
    return (
        area.start.x <= position.x <= area.end.x
        and area.start.y <= position.y <= area.end.y
    )


def perform_step(position: Point, velocity: Point):
    position.x += velocity.x
    position.y += velocity.y

    if velocity.x > 0:
        velocity.x -= 1
    elif velocity.x < 0:
        velocity.x += 1

    velocity.y -= 1


def hits_target(velocity: Point, target: Area, statistics: ProbeStatistics) -> bool:
    position = Point(0, 0)
    max_altitude = 0

    while True:
        perform_step(position, velocity)

        max_altitude = max(max_altitude, position.y)

        if is_in_area(position, target):
            statistics.hit_counter += 1
            statistics.max_altitude = max(statistics.max_altitude, max_altitude)
            return True

        # If y is negative and if we are past the end y coordinate we can never reach the target
        if velocity.y <= 0 and position.y < target.start.y:
            return False


def main():
    # Part 1 & 2
    target_area = read_input('input.txt')

    # An x velocity of zero or lower will never reach the target since the x velocity cannot increase past zero
    # therefore it is set to 1. The maximum velocity was arbitrarily chosen.
    vx_range = range(1, 300)

    # A y velocity lower than the minimum the y start position will shoot past the target area after one step. The
    # maximum y velocity was arbitrarily chosen.
    vy_range = range(target_area.start.y, 300)

    stats = ProbeStatistics()
    for y in vy_range:
        for x in vx_range:
            velocity = Point(x, y)
            hits_target(velocity, target_area, stats)

    print(stats.max_altitude)
    assert stats.max_altitude == 6555

    print(stats.hit_counter)
    assert stats.hit_counter == 4973


if __name__ == '__main__':
    main()

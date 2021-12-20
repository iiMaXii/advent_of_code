"""Advent of Code 2021 - Day 19

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
from typing import List
from typing import Optional
from typing import Tuple

import re
from collections import Counter
from collections import defaultdict
from dataclasses import dataclass
from math import cos
from math import sin
from math import radians

Vector = Tuple[int, int, int]


@dataclass(frozen=True)
class Sensor:
    rotation: List[Vector]
    distance: List[Vector]
    readings: List[Vector]
    number: int


def read_input(filename: str) -> Dict[int, List[Vector]]:
    with open(filename) as f:
        lines = f.readlines()

    sensor_number = None
    scanners = defaultdict(list)
    for line in lines:
        line = line.strip()
        if not line:
            continue

        m = re.match(r'--- scanner (\d+) ---', line)
        if m:
            sensor_number = int(m.group(1))
        else:
            assert sensor_number is not None
            x, y, z = [int(c) for c in line.split(',')]
            scanners[sensor_number].append((x, y, z))

    return scanners


def vector_add(v1: Vector, v2: Vector) -> Vector:
    return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]


def vector_subtract(v1: Vector, v2: Vector) -> Vector:
    return v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]


def vector_rotate(v: Vector, rotation_vector: Vector) -> Vector:
    x_degrees, y_degrees, z_degrees = rotation_vector

    if x_degrees:
        x, y, z = v
        theta = radians(x_degrees)
        v = (
            round(x * cos(theta) - y * sin(theta)),
            round(x * sin(theta) + y * cos(theta)),
            z,
        )

    if y_degrees:
        x, y, z = v
        theta = radians(y_degrees)
        v = (
            round(x * cos(theta) + z * sin(theta)),
            y,
            round(-x * sin(theta) + z * cos(theta)),
        )

    if z_degrees:
        x, y, z = v
        theta = radians(z_degrees)
        v = (
            x,
            round(y * cos(theta) - z * sin(theta)),
            round(y * sin(theta) + z * cos(theta)),
        )

    return v


def vector_manhattan_distance(v1: Vector, v2: Vector):
    return sum([abs(a - b) for a, b in zip(v1, v2)])


# List of all possible non overlapping rotation vectors
_possible_vector_rotations = [
    (0, 0, 0),
    (0, 0, 90),
    (0, 0, 180),
    (0, 0, 270),
    (0, 90, 0),
    (0, 90, 90),
    (0, 90, 180),
    (0, 90, 270),
    (0, 180, 0),
    (0, 180, 90),
    (0, 180, 180),
    (0, 180, 270),
    (0, 270, 0),
    (0, 270, 90),
    (0, 270, 180),
    (0, 270, 270),
    (90, 0, 0),
    (90, 0, 90),
    (90, 0, 180),
    (90, 0, 270),
    (90, 180, 0),
    (90, 180, 90),
    (90, 180, 180),
    (90, 180, 270),
]


def all_vector_rotations(data: List[Vector]):
    """Generate all possible vector rotation for the list."""
    for rotation_vector in _possible_vector_rotations:
        yield rotation_vector, [vector_rotate(v, rotation_vector) for v in data]


def find_distance_by_common_readings(reference: List[Vector], other: List[Vector]):
    """Find sensor distance and rotation if they have at least 12 common readings."""
    found_rotation_vector = None
    found_distance_diff = None

    for rotation_vector, rotated_vector_list in all_vector_rotations(other):
        total = []
        for v1 in reference:
            total.extend([vector_subtract(v1, v2) for v2 in rotated_vector_list])

        diff, count = Counter(total).most_common(1)[0]
        if count >= 12:
            assert not found_rotation_vector
            found_distance_diff = diff
            found_rotation_vector = rotation_vector

    return found_rotation_vector, found_distance_diff


def calculate_adjacent_sensors(reference, data) -> Dict[int, Tuple[Vector, Vector]]:
    result = {}
    for sensor_number, other in data.items():
        rotation_vector, distance_diff = find_distance_by_common_readings(
            reference, other
        )
        if rotation_vector:
            result[sensor_number] = (rotation_vector, distance_diff)
    return result


def calculate_actual_distance_reference(distance: Vector, sensor: Sensor) -> Vector:
    for d, r in zip(reversed(sensor.distance), reversed(sensor.rotation)):
        distance = vector_rotate(distance, r)
        distance = vector_add(distance, d)
    return distance


def calculate_actual_distance(distance: Vector, sensor: Sensor) -> Vector:
    for d, r in zip(reversed(sensor.distance[:-1]), reversed(sensor.rotation[:-1])):
        distance = vector_rotate(distance, r)
        distance = vector_add(distance, d)
    return distance


def get_sensors(
    data: Dict[int, List[Vector]], reference_sensor: Optional[Sensor] = None
) -> Dict[int, Sensor]:
    result = {}
    if reference_sensor is None:
        data = data.copy()
        reference_sensor = Sensor(
            rotation=[(0, 0, 0)], distance=[(0, 0, 0)], readings=data.pop(0), number=0
        )
        result[0] = reference_sensor

    reference_sensors = []
    for sensor_number, (rotation, distance) in calculate_adjacent_sensors(
        reference_sensor.readings, data
    ).items():
        act_distance = distance
        for d, r in zip(
            reversed(reference_sensor.distance), reversed(reference_sensor.rotation)
        ):
            act_distance = vector_rotate(act_distance, r)
            act_distance = vector_add(act_distance, d)

        sensor = Sensor(
            rotation=reference_sensor.rotation + [rotation],
            distance=reference_sensor.distance + [distance],
            readings=data.pop(sensor_number),
            number=sensor_number,
        )
        result[sensor_number] = sensor
        reference_sensors.append(sensor)

    for ref in reference_sensors:
        result.update(get_sensors(data, ref))

    return result


def main():
    # Part 1
    data = read_input('input.txt')

    all_readings = set()
    sensors = get_sensors(data)
    for n, sensor in sensors.items():
        for reading in sensor.readings:
            all_readings.add(calculate_actual_distance_reference(reading, sensor))

    result = len(all_readings)
    print(result)
    assert result == 457

    # Part 2
    distances = []
    for s1 in sensors.values():
        for s2 in sensors.values():
            d1 = calculate_actual_distance(s1.distance[-1], s1)
            d2 = calculate_actual_distance(s2.distance[-1], s2)
            distances.append(vector_manhattan_distance(d1, d2))

    result = max(distances)
    print(result)
    assert result == 13243


if __name__ == '__main__':
    main()

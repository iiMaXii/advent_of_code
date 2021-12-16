"""Advent of Code 2021 - Day 16

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
from typing import Iterable

from dataclasses import dataclass
from io import StringIO


def parse_hex(data: str) -> str:
    return ''.join([f'{int(r, 16):04b}' for r in data.strip()])


def read_input(filename: str) -> str:
    with open(filename) as f:
        lines = f.readlines()

    return parse_hex(lines[0])


@dataclass
class PacketStatistics:
    packet_version_sum: int = 0

    def add_stat(self, packet_version: int):
        self.packet_version_sum += packet_version


def prod(iterable: Iterable[int]) -> int:
    product = 1
    for n in iterable:
        product *= n
    return product


operators = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda l: 1 if l[0] > l[1] else 0,
    6: lambda l: 1 if l[0] < l[1] else 0,
    7: lambda l: 1 if l[0] == l[1] else 0,
}


def parse_packet(
    data: StringIO, packet_statistics: Optional[PacketStatistics] = None
) -> int:
    packet_version = int(data.read(3), 2)
    packet_type = int(data.read(3), 2)

    if packet_statistics:
        packet_statistics.add_stat(packet_version)

    if packet_type == 4:
        # Literal
        value_bits = []
        more_data_bit = '1'
        while more_data_bit == '1':
            more_data_bit = data.read(1)
            value_bits.append(data.read(4))
        return int(''.join(value_bits), 2)
    else:
        # Operator
        values = []
        length_type = data.read(1)
        if length_type == '0':
            sub_packet_length = int(data.read(15), 2)
            end_position = data.tell() + sub_packet_length
            while data.tell() < end_position:
                values.append(parse_packet(data, packet_statistics))
        else:
            sub_packet_count = int(data.read(11), 2)
            for _ in range(sub_packet_count):
                values.append(parse_packet(data, packet_statistics))

        f = operators.get(packet_type, None)
        if f is None:
            raise NotImplementedError(packet_type)

        return f(values)


def main():
    examples = [
        ('C200B40A82', 3),
        ('04005AC33890', 54),
        ('880086C3E88112', 7),
        ('CE00C43D881120', 9),
        ('D8005AC2A8F0', 1),
        ('F600BC2D8F', 0),
        ('9C005AC2F8F0', 0),
        ('9C0141080250320F1802104A08', 1),
    ]

    for data, solution in examples:
        result = parse_packet(StringIO(parse_hex(data)))
        assert solution == result

    # Part 1 & 2
    data = read_input('input.txt')

    packet_statistics = PacketStatistics()
    result = parse_packet(StringIO(data), packet_statistics)

    print(packet_statistics.packet_version_sum)
    assert packet_statistics.packet_version_sum == 897

    print(result)
    assert result == 9485076995911


if __name__ == '__main__':
    main()

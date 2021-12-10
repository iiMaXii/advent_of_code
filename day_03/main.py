"""Advent of Code 2021 - Day 3

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
from typing import Any
from typing import Iterable
from typing import List

from collections import Counter


def read_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def transpose_input_data(data: List[Iterable[Any]]) -> List[List[Any]]:
    result = [[] for _ in data[0]]
    for row in data:
        for i, b in enumerate(row):
            result[i].append(b)

    return result


def get_counters(data: List[str]) -> List[Counter]:
    data = transpose_input_data(data)
    return [Counter(v) for v in data]


def common_bits(data: List[str], type: str) -> str:
    if type not in ['most', 'least']:
        raise ValueError()

    result = []
    for c in get_counters(data):
        assert c['0'] != c['1']
        comparison = c['0'] > c['1']

        if type == 'least':
            # yeah, ugly I know :/
            comparison = not comparison

        result.append('0' if comparison else '1')
    return ''.join(result)


def get_after_bit_crit(data: List[str], condition: str) -> str:
    if condition not in ['most', 'least']:
        raise ValueError()

    for index, _ in enumerate(data[0]):
        counter = get_counters(data)[index]

        if condition == 'most':
            filter_bit = '0' if counter['0'] > counter['1'] else '1'
        else:
            filter_bit = '0' if counter['0'] <= counter['1'] else '1'

        data = [v for v in data if v[index] == filter_bit]

        if len(data) == 1:
            # We're done here
            return data[0]

    raise Exception()


def main():
    data = read_input('input.txt')

    # Part 1
    gamma_bits = common_bits(data, 'most')
    gamma_rate = int(gamma_bits, 2)

    epsilon_bits = common_bits(data, 'least')
    epsilon_rate = int(epsilon_bits, 2)

    power_consumption = gamma_rate * epsilon_rate

    print(f'gamma_rate={gamma_rate}')
    print(f'epsilon_rate={epsilon_rate}')
    print(f'power_consumption{power_consumption}')

    assert power_consumption == 1307354

    # Part 2
    oxygen_generator_bits = get_after_bit_crit(data, 'most')
    oxygen_generator_rating = int(oxygen_generator_bits, 2)

    co2_scrubber_bits = get_after_bit_crit(data, 'least')
    co2_scrubber_rating = int(co2_scrubber_bits, 2)

    life_support_rating = oxygen_generator_rating * co2_scrubber_rating

    print(f'oxygen_generator_rating={oxygen_generator_rating}')
    print(f'co2_scrubber_rating={co2_scrubber_rating}')
    print(f'life_support_rating={life_support_rating}')

    assert life_support_rating == 482500


if __name__ == '__main__':
    main()

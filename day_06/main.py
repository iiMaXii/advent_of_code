"""Advent of Code 2021 - Day 6

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

from collections import Counter


def read_input(filename: str) -> List[int]:
    with open(filename) as f:
        lines = f.readlines()

    return [int(v) for v in lines[0].strip().split(',')]


def perform_cycle(state: List[int] = None):
    new_fish_count = 0

    for index, v in enumerate(state):
        if v == 0:
            # reset timer
            state[index] = 6

            new_fish_count += 1
        else:
            state[index] -= 1

    for _ in range(new_fish_count):
        state.append(8)


def get_state_dict(state: List[int]) -> Dict[int, int]:
    return dict(Counter(state))


def perform_cycle_dict(state: Dict[int, int]):
    new_fish_count = 0

    new_state = {}
    for v, count in state.items():
        if v == 0:
            # reset timer
            new_state[6] = count

            new_fish_count += count
        else:
            if (v - 1) in new_state:
                new_state[v - 1] += count
            else:
                new_state[v - 1] = count

    if new_fish_count:
        new_state[8] = new_fish_count

    return new_state


def main():
    # Part 1
    data = read_input('input.txt')

    for day in range(80):
        perform_cycle(data)

    lanternfish_count = len(data)
    print(f'lanternfish_count={lanternfish_count}')

    # Part 2
    data = read_input('input.txt')
    states = get_state_dict(data)

    for day in range(256):
        states = perform_cycle_dict(states)

    lanternfish_count = sum([v for v in states.values()])
    print(f'lanternfish_count={lanternfish_count}')
    assert lanternfish_count == 1740449478328


if __name__ == '__main__':
    main()

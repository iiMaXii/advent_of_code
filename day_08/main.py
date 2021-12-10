"""Advent of Code 2021 - Day 8

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


def read_input(filename: str):
    with open(filename) as f:
        lines = f.readlines()

    result = []
    for line in lines:
        line = line.strip()

        input_values, output_values = line.split('|')

        result.append((input_values.strip().split(), output_values.strip().split()))

    return result


numbers_7_seg = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}


class SegDisplaySolver:
    def __init__(self):
        self.comb: Dict[str, List] = {l: list('abcdefg') for l in list('abcdefg')}

    def remove_simple(self, lit_segments, possible_endpoints):
        unlit_segments = [c for c in 'abcdefg' if c not in lit_segments]
        for s in unlit_segments:
            for l in possible_endpoints:
                try:
                    self.comb[s].remove(l)
                except ValueError:
                    pass  # ignore not in list

        for s in list(lit_segments):
            self.comb[s] = [c for c in self.comb[s] if c in possible_endpoints]

    def give_hint(self, lit_segments: str):
        if len(lit_segments) == 2:
            # 1
            self.remove_simple(lit_segments, 'cf')
        elif len(lit_segments) == 3:
            # 7
            self.remove_simple(lit_segments, 'acf')
        elif len(lit_segments) == 4:
            # 4
            self.remove_simple(lit_segments, 'bcdf')
        elif len(lit_segments) == 7:
            # 8
            # no useful information
            pass

    def run(self, data):
        for comb in data:
            self.give_hint(comb)


def all_combinations(comb):
    # not my proudest moment
    for a in comb['a']:
        for b in comb['b']:
            for c in comb['c']:
                for d in comb['d']:
                    for e in comb['e']:
                        for f in comb['f']:
                            for g in comb['g']:
                                yield {
                                    'a': a,
                                    'b': b,
                                    'c': c,
                                    'd': d,
                                    'e': e,
                                    'f': f,
                                    'g': g,
                                }


def get_number(lit_segments, solution):
    real_lit_segments = [solution[l] for l in lit_segments]

    if len(real_lit_segments) != len(set(real_lit_segments)):
        return None

    real_lit_segments = ''.join(sorted(real_lit_segments))

    for number, lit_seg in numbers_7_seg.items():
        if real_lit_segments == lit_seg:
            return number

    return None


def is_solution(values, solution):
    for v in values:
        n = get_number(v, solution)

        if n is None:
            return False

    return True


def main():
    # Part 1
    data = read_input('input.txt')

    counter = 0
    for input_values, output_values in data:
        for v in output_values:
            if len(v) in [2, 4, 3, 7]:
                counter += 1

    print(counter)
    assert counter == 412

    # Part 2
    total_sum = 0
    for input_values, output_values in data:
        solver = SegDisplaySolver()
        solver.run(input_values)

        # Brute force combinations
        solution_count = 0
        for solution in all_combinations(solver.comb):
            if is_solution(input_values, solution):
                solution_count += 1

                partial_sum = ''.join(
                    [str(get_number(v, solution)) for v in output_values]
                )
                total_sum += int(partial_sum)

        assert solution_count == 1

    print(total_sum)
    assert total_sum == 978171


if __name__ == '__main__':
    main()

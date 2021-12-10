"""Advent of Code 2021 - Day 10

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


def read_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    result = []
    for line in lines:
        result.append(line.strip())

    return result


parenthesis = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

score_table = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def calculate_syntax_error_score(data: str) -> int:
    score = 0
    stack = []
    for c in data:
        if c in '({[<':
            stack.append(c)
        elif c in ')]}>':
            expected_end = parenthesis[stack.pop()]
            if c != expected_end:
                score += score_table[c]

        else:
            raise ValueError(c)
    return score


score_table_v2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def calculate_incomplete_score(data: str) -> int:
    score = 0
    stack = []
    for c in data:
        if c in '({[<':
            stack.append(c)
        elif c in ')]}>':
            expected_end = parenthesis[stack.pop()]
            assert c == expected_end

        else:
            raise ValueError(c)

    try:
        while True:
            c = stack.pop()
            score = score * 5 + score_table_v2[parenthesis[c]]
    except IndexError:
        pass  # done

    return score


def main():
    # Part 1
    data = read_input('input.txt')

    result = sum([calculate_syntax_error_score(l) for l in data])
    print(result)
    assert result == 464991

    # Part 2
    incomplete_lines = [l for l in data if calculate_syntax_error_score(l) == 0]

    incomplete_scores = sorted(
        [calculate_incomplete_score(l) for l in incomplete_lines]
    )
    index = (len(incomplete_scores) - 1) / 2
    result = incomplete_scores[int(index)]
    print(result)
    assert result == 3662008566


if __name__ == '__main__':
    main()

"""Advent of Code 2021 - Day 4

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
from typing import List
from typing import Tuple

from dataclasses import dataclass
from dataclasses import field


@dataclass
class BingoSquare:
    number: int
    checked: bool = False


def transpose_input_data(data: List[List[Any]]) -> List[List[Any]]:
    result = [[] for _ in data[0]]
    for row in data:
        for i, b in enumerate(row):
            result[i].append(b)

    return result


@dataclass
class BingoBoard:
    rows: List[List[BingoSquare]] = field(default_factory=list)
    col_count: int = 5
    row_count: int = 5

    last_marked_number: int = None

    def mark_number(self, number: int):
        self.last_marked_number = number
        for row in self.rows:
            for square in row:
                if square.number == number:
                    square.checked = True

    def score(self) -> int:
        unmarked_numbers: List[int] = []
        for row in self.rows:
            for square in row:
                if not square.checked:
                    unmarked_numbers.append(square.number)

        return self.last_marked_number * sum(unmarked_numbers)

    def has_won(self) -> bool:
        # Check rows
        for row in self.rows:
            if all([n.checked for n in row]):
                return True

        # Check columns
        columns = transpose_input_data(self.rows)
        for col in columns:
            if all([n.checked for n in col]):
                return True

        return False


def read_input(filename: str) -> Tuple[List[int], List[BingoBoard]]:
    drawn_numbers: List[int] = []
    bingo_boards: List[BingoBoard] = []

    with open(filename) as f:
        lines = f.readlines()
        drawn_numbers = [int(n) for n in lines[0].strip().split(',')]

        bingo_board = BingoBoard()
        for line in lines[2:]:
            line = line.strip()

            if not line:
                assert len(bingo_board.rows) == 5
                bingo_boards.append(bingo_board)
                bingo_board = BingoBoard()
                continue

            row = [int(n) for n in line.split()]
            assert len(row) == 5

            bingo_board.rows.append([BingoSquare(n) for n in row])

        assert len(bingo_board.rows) == 5
        bingo_boards.append(bingo_board)

    return drawn_numbers, bingo_boards


def get_first_winner_score(drawn_numbers, bingo_boards) -> int:
    for drawn_number in drawn_numbers:
        for bingo_board in bingo_boards:
            bingo_board.mark_number(drawn_number)

            if bingo_board.has_won():
                return bingo_board.score()


def get_last_winner_score(drawn_numbers: List[int], bingo_boards: List[BingoBoard]) -> int:
    for drawn_number in drawn_numbers:
        for bingo_board in bingo_boards:
            bingo_board.mark_number(drawn_number)

        # End condition
        if len(bingo_boards) == 1 and bingo_boards[0].has_won():
            return bingo_boards[0].score()

        # Remove boards that have won
        bingo_boards = [b for b in bingo_boards if not b.has_won()]

    raise ValueError()


def main():
    drawn_numbers, bingo_boards = read_input('input.txt')

    # Part 1
    score = get_first_winner_score(drawn_numbers, bingo_boards)
    assert score == 49686
    print(score)

    # Part 2
    drawn_numbers, bingo_boards = read_input('input.txt')  # Reset data

    score = get_last_winner_score(drawn_numbers, bingo_boards)
    assert score == 26878
    print(score)


if __name__ == '__main__':
    main()

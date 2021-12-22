"""Advent of Code 2021 - Day 21

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

import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import cycle


@dataclass
class Player:
    number: int
    position: int
    score: int = 0


def read_input(filename: str) -> List[Player]:
    with open(filename) as f:
        lines = f.readlines()

    r = []
    for line in lines:
        m = re.match(r'Player (\d+) starting position: (\d+)', line.strip())
        r.append(Player(int(m.group(1)), int(m.group(2))))

    return r


def all_rolls():
    for d1 in [1, 2, 3]:
        for d2 in [1, 2, 3]:
            for d3 in [1, 2, 3]:
                yield d1 + d2 + d3


def main():
    players = read_input('input.txt')

    # Part 1
    die_roll_count = 0
    die = cycle(range(1, 11))

    while all([p.score < 1000 for p in players]):
        for p in players:
            move_count = next(die) + next(die) + next(die)
            die_roll_count += 3

            p.position = (p.position + move_count - 1) % 10 + 1
            p.score += p.position
            # print(f'Player {p.number} moves {move_count}, to {p.position}, score {p.score}')

            if p.score >= 1000:
                break

    lowest_score = min([p.score for p in players])
    result = lowest_score * die_roll_count
    print(result)
    assert result == 506466

    # Part 2
    players = read_input('input.txt')  # reset

    score_position_count_dict = defaultdict(int)
    score_position_count_dict[
        (
            0,  # Player 1 score
            players[0].position,  # Player 1 position
            0,  # Player 2 score
            players[1].position,  # Player 2 position
        )
    ] = 1  # Universe count
    p1_turn = True

    p1_wins = 0
    p2_wins = 0
    while score_position_count_dict:
        new_dict = defaultdict(int)
        for (
            p1_score,
            p1_position,
            p2_score,
            p2_position,
        ), universe_count in score_position_count_dict.items():
            if p1_turn:
                for roll in all_rolls():
                    new_pos = (p1_position + roll - 1) % 10 + 1
                    new_score = p1_score + new_pos
                    if new_score >= 21:
                        p1_wins += universe_count
                    else:
                        new_dict[
                            (new_score, new_pos, p2_score, p2_position)
                        ] += universe_count
            else:
                for roll in all_rolls():
                    new_pos = (p2_position + roll - 1) % 10 + 1
                    new_score = p2_score + new_pos
                    if new_score >= 21:
                        p2_wins += universe_count
                    else:
                        new_dict[
                            (p1_score, p1_position, new_score, new_pos)
                        ] += universe_count

        score_position_count_dict = new_dict
        p1_turn = not p1_turn

    result = max(p1_wins, p2_wins)
    print(result)
    assert result == 632979211251440


if __name__ == '__main__':
    main()

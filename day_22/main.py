"""Advent of Code 2021 - Day 22

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
from typing import Optional

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def size(self) -> int:
        return (
            (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)
        )


@dataclass(frozen=True)
class Step:
    turn_on: bool
    region: Region


def read_input(filename: str) -> List[Step]:
    with open(filename) as f:
        lines = f.readlines()

    r = []
    for line in lines:
        m = re.match(
            r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)',
            line.strip(),
        )
        s = Step(m.group(1) == 'on', Region(*[int(n) for n in m.groups()[1:]]))
        r.append(s)

    return r


def clamp_region_50_50(region: Region) -> Optional[Region]:
    """Clamp the region to x=-50..50, y=-50..50, z=-50..50."""
    if (
        region.x1 > 50
        or region.x2 < -50
        or region.y1 > 50
        or region.y2 < -50
        or region.z1 > 50
        or region.z2 < -50
    ):
        return None  # out of range

    return Region(
        max(region.x1, -50),
        min(region.x2, 50),
        max(region.y1, -50),
        min(region.y2, 50),
        max(region.z1, -50),
        min(region.z2, 50),
    )


def get_start_coord(r1_c1: int, r1_c2: int, r2_c1: int) -> int:
    if r1_c1 <= r2_c1 <= r1_c2:
        return r2_c1
    elif r2_c1 < r1_c1:
        return r1_c1
    else:
        assert False, 'Should be checked by condition'


def get_end_coord(r1_c1: int, r1_c2: int, r2_c2: int) -> int:
    if r1_c1 <= r2_c2 <= r1_c2:
        return r2_c2
    elif r2_c2 > r1_c2:
        return r1_c2
    else:
        assert False, 'Should be checked by condition'


def intersection(r1: Region, r2: Region) -> Optional[Region]:
    if (
        r1.x1 > r2.x2
        or r1.x2 < r2.x1
        or r1.y1 > r2.y2
        or r1.y2 < r2.y1
        or r1.z1 > r2.z2
        or r1.z2 < r2.z1
    ):
        return None  # no intersection

    return Region(
        get_start_coord(r1.x1, r1.x2, r2.x1),
        get_end_coord(r1.x1, r1.x2, r2.x2),
        get_start_coord(r1.y1, r1.y2, r2.y1),
        get_end_coord(r1.y1, r1.y2, r2.y2),
        get_start_coord(r1.z1, r1.z2, r2.z1),
        get_end_coord(r1.z1, r1.z2, r2.z2),
    )


def main():
    steps = read_input('input.txt')

    # Part 1
    active_cubes = set()
    for step in steps:
        clamped_region = clamp_region_50_50(step.region)
        if not clamped_region:
            continue

        for z in range(clamped_region.z1, clamped_region.z2 + 1):
            for y in range(clamped_region.y1, clamped_region.y2 + 1):
                for x in range(clamped_region.x1, clamped_region.x2 + 1):
                    if step.turn_on:
                        active_cubes.add((x, y, z))
                    else:
                        try:
                            active_cubes.remove((x, y, z))
                        except KeyError:
                            pass

    result = len(active_cubes)
    print(result)
    assert result == 580098

    # Part 2
    """
    The previous approach will no longer work since we have too many points for our computer to handle. Instead we
    realise that we can use the intersection between the regions. Consider the following example with three overlapping
    regions:
    
                   +--------------------+
                   |                    |
                   |         B          |
    +--------------+----------+         |
    |              |          |         |
    |              |     +----+---------+--------+
    |          A   |     |    |         |        |
    |              +-----+----+---------+        |
    |                    |    |                  |
    +--------------------+----+      C           |
                         |                       |
                         |                       |
                         +-----------------------+

    We can derive the *on* (add) and *off* (remove) action from this.
    
    Terminology
    -----------
    * |A| means cube count in A (https://en.wikipedia.org/wiki/Cardinality)
    * A∩B means the intersection (https://en.wikipedia.org/wiki/Intersection_(set_theory))
    
    On action (add)
    ---------------
    Assume we have the following steps:
    1. Turn on all in A
    2. Turn on all in B
    3. Turn on all in C
    
    So let's begin:
    1. The first step is pretty simple:
       result = |A|
    
    2. Now we need to take care of the intersection by removing it so it isn't counted twice:
       result = |A| + |B| - |A∩B|
    
    3. This follows the same procedure as in step 2, but we also take the intersection between A and B into account:
       result = |A| + |B| - |A∩B| + |C| - |A∩C| - |B∩C| - (-|(A∩B)∩C|)
              = |A| + |B| - |A∩B| + |C| - |A∩C| - |B∩C| + |(A∩B)∩C|
    
    Off action (remove)
    -------------------
    Assume we have the following steps:
    1. Turn on all in A
    2. Turn on all in B
    3. Turn *off* all in C
    
    Step 1 and 2 are identical to the previous example. But in step 3 we have the off or remove action. We only want to
    remove the intersections and also take care not to count anything more than once.
    
    We realise that we already removed the intersecting sections in the previous example in step 3. The modified step 3
    will therefore look like this:
    result = |A| + |B| - |A∩B| - |A∩C| - |B∩C| + |(A∩B)∩C|
    
    Note that we only removed |C|.
    
    These actions are implemented below.
    """

    positive_terms = []
    negative_terms = []
    for step in steps:
        new_positive_terms = []
        new_negative_terms = []

        if step.turn_on:
            new_positive_terms.append(step.region)

        for positive_term in positive_terms:
            i = intersection(positive_term, step.region)
            if i:
                new_negative_terms.append(i)

        for negative_term in negative_terms:
            i = intersection(negative_term, step.region)
            if i:
                new_positive_terms.append(i)

        positive_terms.extend(new_positive_terms)
        negative_terms.extend(new_negative_terms)

    result = sum([p.size() for p in positive_terms]) - sum(
        [n.size() for n in negative_terms]
    )
    print(result)
    assert result == 1134725012490723


if __name__ == '__main__':
    main()

import pytest
from dataclasses import dataclass

from search import search
from input import T_poly


@dataclass
class SearchCase:
    D: tuple[int, int]
    rec: list[T_poly]
    arc: list[T_poly]
    expected: bool

TEST_CASES = [
    SearchCase(
        D=(4, 6),
        rec=[],
        arc=[],
        expected=True
    ),
    SearchCase(
        D=(4, 4),
        rec=[((2, 2), 2)],
        arc=[],
        expected=True
    ),
    SearchCase(
        D=(4, 4),
        rec=[((2, 2), 4)],
        arc=[],
        expected=True
    ),
    SearchCase(
        D=(4, 3),
        rec=[((2, 2), 4)],
        arc=[],
        expected=False
    ),
    SearchCase(
        D=(4, 4),
        rec=[((4, 4), 1)],
        arc=[],
        expected=True
    ),
    SearchCase(
        D=(4, 3),
        rec=[((4, 4), 1)],
        arc=[],
        expected=False
    ),
    SearchCase(
        D=(4, 5),
        rec=[((4, 4), 1)],
        arc=[],
        expected=True
    ),
    SearchCase(
        D=(3, 4),
        rec=[],
        arc=[((4, 3), 1)],
        expected=True
    ),
    SearchCase(
        D=(4, 3),
        rec=[],
        arc=[((4, 3), 1)],
        expected=True
    ),
    SearchCase(
        D=(3, 3),
        rec=[],
        arc=[((4, 3), 1)],
        expected=False
    ),
    SearchCase(
        D=(3, 4),
        rec=[],
        arc=[((2, 3), 2)],
        expected=True
    ),
    SearchCase(
        D=(3, 4),
        rec=[((1, 2), 1)],
        arc=[((2, 3), 2)],
        expected=True
    ),
    SearchCase(
        D=(3, 4),
        rec=[((1, 3), 1)],
        arc=[((2, 3), 2)],
        expected=False
    ),
    SearchCase(
        D=(3, 4),
        rec=[((1, 1), 2)],
        arc=[((2, 3), 2)],
        expected=True
    ),
    SearchCase(
        D=(4, 6),
        rec=[((2, 2), 2)],
        arc=[((3, 4), 1), ((2, 3), 1)],
        expected=True
    ),
]


@pytest.mark.parametrize('case', TEST_CASES)
def test(case: SearchCase):
    result = search(case.D, case.rec, case.arc)
    assert result == case.expected

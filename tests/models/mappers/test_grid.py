import pytest
from sudoku_strategy.grid import Cell, CellCandidates

from sudoku.models.grid import Digits as ApiDigits
from sudoku.models.grid import Grid as ApiGrid
from sudoku.models.mappers.grid import (
    map_api_digits_to_grid,
    map_api_grid_to_domain,
    map_domain_candidates_to_api,
)


@pytest.fixture
def empty_api_grid():
    return ApiGrid(
        puzzle_digits=[0] * 81,
        digits=[0] * 81,
        candidates=[[] for _ in range(81)],
    )


def test_map_api_grid_to_domain_maps_digits(empty_api_grid):
    # ARRANGE
    empty_api_grid.digits[5] = 7

    # ACT
    result = map_api_grid_to_domain(empty_api_grid)

    # ASSERT
    assert result.analyse.get_digit_in_cell(Cell(5)) == 7


def test_map_api_grid_to_domain_will_not_add_candidates_where_a_digit_is_set(
    empty_api_grid,
):
    # ARRANGE
    empty_api_grid.digits[3] = 5
    empty_api_grid.candidates[3] = [1, 5, 8]

    # ACT
    result = map_api_grid_to_domain(empty_api_grid)

    # ASSERT
    assert result.analyse.get_digit_in_cell(Cell(3)) == 5
    assert len(result.analyse.get_candidates_for_cell(Cell(3))) == 0


def test_map_api_grid_to_domain_maps_candidates(empty_api_grid):
    # ARRANGE
    empty_api_grid.candidates[9] = [4, 6, 8]

    # ACT
    result = map_api_grid_to_domain(empty_api_grid)

    # ASSERT
    candidates = result.analyse.get_candidates_for_cell(Cell(9))
    assert all(candidate in candidates for candidate in (4, 6, 8))


def test_map_api_digits_to_grid():
    # ARRANGE
    # fmt: off
    digits = [
        5, 3, 4, 6, 7, 8, 9, 1, 2,
        6, 0, 2, 1, 9, 5, 3, 4, 8,
        1, 9, 8, 3, 4, 2, 5, 6, 7,
        8, 5, 9, 7, 0, 1, 4, 2, 3,
        4, 2, 6, 8, 5, 3, 7, 9, 1,
        7, 1, 3, 9, 2, 0, 8, 5, 6,
        9, 6, 1, 5, 3, 7, 2, 8, 4,
        0, 8, 7, 4, 1, 9, 6, 3, 5,
        3, 4, 5, 2, 8, 6, 1, 7, 9
    ]
    # fmt: on

    api_digits = ApiDigits(digits=digits)

    # ACT
    result = map_api_digits_to_grid(api_digits)

    # ASSERT
    for cell in result.analyse.cell_groups.cells():
        assert result.analyse.get_digit_in_cell(cell) == digits[cell.index]


def test_map_domain_candidates_to_api():
    # ARRANGE
    candidates = (CellCandidates(i) for i in range(81))

    # ACT
    result = map_domain_candidates_to_api(candidates)

    # ASSERT
    assert len(result.candidates) == 81
    assert all(isinstance(candidates, list) for candidates in result.candidates)
    assert all(
        1 <= digit <= 9 for candidates in result.candidates for digit in candidates
    )

    assert result.candidates[0] == []
    assert result.candidates[1] == [1]
    assert result.candidates[2] == [2]
    assert result.candidates[3] == [1, 2]

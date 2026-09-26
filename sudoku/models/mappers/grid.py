from typing import TYPE_CHECKING

from sudoku_strategy import Grid as DomainGrid
from sudoku_strategy.grid import CellCandidates

from ..grid import Candidates as ApiCandidates
from ..grid import Digits as ApiDigits
from ..grid import Grid as ApiGrid

if TYPE_CHECKING:
    from collections.abc import Iterable


def map_api_grid_to_domain(api_grid: ApiGrid) -> DomainGrid:
    grid = DomainGrid.new_puzzle(tuple(api_grid.puzzle_digits))

    for cell in grid.analyse.cell_groups.cells():
        digit = api_grid.digits[cell.index]
        if digit != 0:
            grid.modify.write_digit(digit, cell)
        else:
            candidates = api_grid.candidates[cell.index]
            grid.modify.add_candidates(candidates, cell)

    return grid


def map_api_digits_to_grid(digits: ApiDigits) -> DomainGrid:
    return DomainGrid.new_puzzle(tuple(digits.digits))


def map_domain_candidates_to_api(candidates: Iterable[CellCandidates]) -> ApiCandidates:
    return ApiCandidates(candidates=list(map(list, candidates)))

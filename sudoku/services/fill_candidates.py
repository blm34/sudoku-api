from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_strategy import Grid
    from sudoku_strategy.grid import CellCandidates


class CandidatesService:
    def compute_candidates(self, grid: Grid) -> list[CellCandidates]:
        grid.modify.compute_candidates()
        return grid._state.cell_candidates

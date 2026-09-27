from typing import Annotated

from fastapi import APIRouter, Depends

from sudoku.models.grid import Candidates, Digits
from sudoku.models.mappers.grid import (
    map_api_digits_to_grid,
    map_domain_candidates_to_api,
)
from sudoku.services.fill_candidates import CandidatesService

router = APIRouter()


def get_candidates_service() -> CandidatesService:
    return CandidatesService()


CandidatesServiceDependency = Annotated[
    CandidatesService,
    Depends(get_candidates_service),
]


@router.post("/fill_candidates", response_model=Candidates)
def fill_candidates(
    digits: Digits,
    candidates_service: CandidatesServiceDependency,
):
    grid = map_api_digits_to_grid(digits)
    candidates = candidates_service.compute_candidates(grid)
    return map_domain_candidates_to_api(candidates)

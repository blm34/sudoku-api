from fastapi import APIRouter

from .compute_candidates import router as compute_candidates_router

router = APIRouter(prefix="/v1")

router.include_router(compute_candidates_router)

__all__ = [
    "router",
]

from fastapi import FastAPI

from sudoku.api import router

app = FastAPI()

app.include_router(router)

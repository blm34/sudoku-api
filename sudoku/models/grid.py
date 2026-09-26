from pydantic import BaseModel, Field, field_validator


class Digits(BaseModel):
    digits: list[int] = Field(
        description="81 digits as within a grid, 0 representing empty."
    )

    @field_validator("digits")
    @classmethod
    def validate_digits(cls, digits: list[int]) -> list[int]:
        if len(digits) != 81:
            raise ValueError(f"There must be 81 digits: {len(digits)} is not valid.")

        if any(not 0 <= digit <= 9 for digit in digits):
            raise ValueError("Digits must be 1-9 (or 0 for unset)")

        return digits


class Candidates(BaseModel):
    candidates: list[list[int]] = Field(description="Candidates for cells.")

    @field_validator("candidates")
    @classmethod
    def validate_candidates(cls, candidates: list[list[int]]) -> list[list[int]]:
        if len(candidates) != 81:
            raise ValueError("There must be candidates for 81 cells")

        if any(digit < 0 or digit > 9 for cell in candidates for digit in cell):
            raise ValueError("Candidate values must be 1-9")

        return candidates


class Grid(BaseModel):
    puzzle_digits: list[int] = Field(
        description="Digits present in the starting puzzle state."
    )
    digits: list[int] = Field(description="Digits present in the current puzzle state.")
    candidates: list[list[int]] = Field(description="Candidates for cells.")

    @field_validator("candidates")
    @classmethod
    def validate_candidates(cls, candidates: list[list[int]]) -> list[list[int]]:
        if len(candidates) != 81:
            raise ValueError("There must be candidates for 81 cells")

        if any(digit < 0 or digit > 9 for cell in candidates for digit in cell):
            raise ValueError("Candidate values must be 1-9")

        return candidates

    @field_validator("puzzle_digits")
    @classmethod
    def validate_puzzle_digits(cls, puzzle_digits: list[int]) -> list[int]:
        if len(puzzle_digits) != 81:
            raise ValueError(
                f"There must be 81 digits: {len(puzzle_digits)} is not valid."
            )

        if any(not 0 <= digit <= 9 for digit in puzzle_digits):
            raise ValueError("Digits must be 1-9 (or 0 for unset)")

        return puzzle_digits

    @field_validator("digits")
    @classmethod
    def validate_digits(cls, digits: list[int]) -> list[int]:
        if len(digits) != 81:
            raise ValueError(f"There must be 81 digits: {len(digits)} is not valid.")

        if any(not 0 <= digit <= 9 for digit in digits):
            raise ValueError("Digits must be 1-9 (or 0 for unset)")

        return digits

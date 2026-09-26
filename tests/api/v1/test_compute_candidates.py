from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from sudoku.api.v1.compute_candidates import get_candidates_service
from sudoku.main import app
from sudoku.services.fill_candidates import CandidatesService


@pytest.fixture
def service():
    return Mock(spec=CandidatesService)


@pytest.fixture
def client(service):
    app.dependency_overrides[get_candidates_service] = lambda: service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_fill_candidates_happy_path(client, service):
    # ARRNAGE
    input_digits = [0] * 81
    expected_candidates = [list(range(1, 10))] * 81
    service.compute_candidates.return_value = expected_candidates

    # ACT
    response = client.post("api/v1/fill_candidates", json={"digits": input_digits})

    # ASSERT
    assert response.status_code == 200
    assert response.json() == {"candidates": expected_candidates}
    service.compute_candidates.assert_called_once()


def test_fill_candidates_rejects_invalid_number_of_digits(client):
    # ARRANGE
    input_digits = [0] * 5

    # ACT
    response = client.post("api/v1/fill_candidates", json={"digits": input_digits})

    # ASSERT
    assert response.status_code == 422


def test_fill_candidates_rejects_invalid_digit(client):
    # ARRANGE
    input_digits = [10] * 81

    # ACT
    response = client.post("api/v1/fill_candidates", json={"digits": input_digits})

    # ASSERT
    assert response.status_code == 422


def test_fill_candidates_rejects_with_no_payload(client):
    # ACT
    response = client.post("api/v1/fill_candidates")

    # ASSERT
    assert response.status_code == 422


def test_fill_candidates_rejects_invalid_json(client):
    # ACT
    response = client.post(
        "/api/v1/fill_candidates",
        content="not json",
        headers={"Content-Type": "application/json"},
    )

    # ASSERT
    assert response.status_code == 422

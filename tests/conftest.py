from fastapi.testclient import TestClient

from src.app import app


def create_test_client() -> TestClient:
    return TestClient(app)


import pytest


@pytest.fixture
def client() -> TestClient:
    return create_test_client()
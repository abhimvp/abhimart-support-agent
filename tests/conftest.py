import os

os.environ["LANGSMITH_TRACING"] = "false"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


def login(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture(scope="session")
def asha(client: TestClient) -> dict[str, str]:
    return login(client, "asha@example.com", "asha-dev-pass")


@pytest.fixture(scope="session")
def ben(client: TestClient) -> dict[str, str]:
    return login(client, "ben@example.com", "ben-dev-pass")

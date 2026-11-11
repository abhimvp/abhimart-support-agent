import pytest

BAD_TOKEN = {"Authorization": "Bearer not.a.real.token"}


@pytest.mark.parametrize(
    "email, password",
    [
        ("asha@example.com", "wrong-password"),
        ("nobody@example.com", "anything"),
    ],
)
def test_bad_login_gets_the_same_401(client, email, password):
    response = client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_customer_can_read_own_order(client, asha, ben):
    assert client.get("/orders/1043", headers=asha).status_code == 200
    assert client.get("/orders/2001", headers=ben).status_code == 200


def test_customer_cannot_read_another_customers_order(client, asha, ben):
    assert client.get("/orders/2001", headers=asha).status_code == 404
    assert client.get("/orders/1043", headers=ben).status_code == 404


@pytest.mark.parametrize("method, path", [("get", "/orders/1043"), ("post", "/chat")])
@pytest.mark.parametrize("headers", [{}, BAD_TOKEN])
def test_requests_without_a_valid_token_are_rejected(client, method, path, headers):
    response = client.request(method, path, headers=headers, json={"message": "hi"})
    assert response.status_code == 401

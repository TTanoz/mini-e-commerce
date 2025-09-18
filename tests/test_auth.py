from tests.factories import auth_token_for, make_user  

def test_register_return_token(client):
    payload = {"email": "a@a.com", "password": "x"}
    res = client.post("/auth/register", json=payload)
    assert res.status_code in (200, 201), res.text
    data = res.json()
    assert "access_token" in data and data["access_token"]

def test_login_works_with_correct_credentials(client):
    token = auth_token_for(client=client)
    assert token is not None

def test_login_fails_with_wrong_password(client):
    client.post(
        "/auth/register",
        json={"email": "u@test.com", "password": "Passw0rd!"},
    )
    res = client.post(
        "/auth/login",
        json={"email": "u@test.com", "password": "Passw0rd!123"},
    )
    assert res.status_code == 401
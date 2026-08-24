def test_register_creates_user(client):
    response = client.post("/auth/register", json={"username": "john", "password": "password123", "role": "viewer"})
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "john"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_username_rejected(client):
    client.post("/auth/register", json={"username": "doe", "password": "password123", "role": "viewer"})
    response = client.post("/auth/register", json={"username": "doe", "password": "password123", "role": "viewer"})
    assert response.status_code == 400


def test_login_with_correct_credentials_returns_token(client):
    client.post("/auth/register", json={"username": "carl", "password": "password123", "role": "viewer"})
    response = client.post("/auth/login", data={"username": "carl", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_wrong_password_rejected(client):
    client.post("/auth/register", json={"username": "martin", "password": "password123", "role": "viewer"})
    response = client.post("/auth/login", data={"username": "martin", "password": "wrongpassword"})
    assert response.status_code == 401


def test_protected_endpoint_without_token_rejected(client):
    response = client.get("/servers")
    assert response.status_code == 401
import pytest


# -----------------------------
# Тест регистрации и логина
# -----------------------------
@pytest.mark.anyio
async def test_register_and_login(client):
    # 1. Регистрация
    response = await client.post(
        "/auth/register/",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "StrongPass123!",
        },
    )
    assert response.status_code == 201
    user_data = response.json()
    user_id = user_data["id"]

    # 2. Логин
    response = await client.post(
        "/auth/login/",
        data={
            "username": "testuser",
            "password": "StrongPass123!",
        },
    )
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    return user_id, tokens["access_token"]  # чтобы использовать в других тестах


@pytest.mark.anyio
async def test_protected_route(client):
    # Регистрация
    response = await client.post(
        "/auth/register/",
        json={
            "username": "testuser2",
            "email": "test2@test.com",
            "password": "StrongPass123!",
        },
    )
    assert response.status_code == 201
    user_data = response.json()
    user_id = user_data["id"]

    # Логин
    login_resp = await client.post(
        "/auth/login/",
        data={"username": "testuser2", "password": "StrongPass123!"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Доступ к защищённому маршруту
    r = await client.get(
        f"/api/users/{user_id}/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser2"
    assert data["email"] == "test2@test.com"

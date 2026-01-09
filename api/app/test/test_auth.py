import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    # 1. Регистрация
    response = await client.post(
        "/api/auth/register/",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "StrongPass123!",
        },
    )
    assert response.status_code == 201

    # 2. Логин
    response = await client.post(
        "/api/auth/login/",
        data={
            "username": "testuser",
            "password": "StrongPass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_protected_route(client):
    login = await client.post(
        "/api/auth/login/",
        data={"username": "test", "password": "StrongPass123!"},
    )
    token = login.json()["access_token"]

    r = await client.get(
        "/api/profile/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200

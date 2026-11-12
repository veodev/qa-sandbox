import uuid

import pytest


@pytest.mark.asyncio
async def test_create_user_success(client, valid_user):
    response = await client.post("/api/v1/users", json=valid_user)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client, valid_user):
    response = await client.post("/api/v1/users", json=valid_user)
    assert response.status_code == 201

    response = await client.post("/api/v1/users", json=valid_user)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_invalid_email(client, user_with_invalid_email):

    response = await client.post("/api/v1/users", json=user_with_invalid_email)

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "email"]
    assert "value is not a valid email address" in data["detail"][0]["msg"].lower()


@pytest.mark.asyncio
async def test_get_user_by_id_success(client, valid_user):
    create_resp = await client.post("/api/v1/users", json=valid_user)
    user_id = create_resp.json()["id"]
    response = await client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client):
    random_uuid = uuid.uuid4()
    response = await client.get(f"/api/v1/users/{random_uuid}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_remove_user_by_id_success(client, valid_user):
    create_resp = await client.post("/api/v1/users", json=valid_user)
    assert create_resp.status_code == 201

    user_id = create_resp.json()["id"]
    remove_resp = await client.delete(f"/api/v1/users/{user_id}")
    assert remove_resp.status_code == 204


@pytest.mark.asyncio
async def test_remove_user_by_id_not_found(client):
    random_uuid = uuid.uuid4()
    response = await client.delete(f"/api/v1/users/{random_uuid}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

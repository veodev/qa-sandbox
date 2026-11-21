import uuid

import requests


def create_user(api_url):
    """Создаёт пользователя и возвращает json с id."""
    email = f"test_{uuid.uuid4().hex[:8]}@test.com"
    payload = {"email": email, "name": "test_user", "password": "test_password"}
    resp = requests.post(f"{api_url}/users", json=payload)
    assert resp.status_code == 201
    return resp.json()


def create_car(api_url, user_id):
    """Создаёт авто пользователя и возвращает json с id."""
    payload = {
        "user_id": user_id,
        "brand": "Toyota",
        "model": "Camry",
        "year": 2022,
        "mileage": 15000,
    }
    resp = requests.post(f"{api_url}/cars", json=payload)
    assert resp.status_code == 201
    return resp.json()


def create_work(api_url, car_id):
    """Создаёт запись о работе для авто и возвращает json с id."""
    payload = {
        "car_id": car_id,
        "description": "Замена масла ДВС и фильтра",
        "mileage": 15000,
        "cost": 1500.0,
        "performed_date": "2024-06-15",
    }
    resp = requests.post(f"{api_url}/works", json=payload)
    assert resp.status_code == 201
    return resp.json()


def assert_status(resp, expected):
    """Проверяет код ответа и бросает AssertionError."""
    assert resp.status_code == expected, (
        f"Expected {expected}, got {resp.status_code}: {resp.text}"
    )

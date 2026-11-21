import json
import uuid

import allure
import requests


@allure.feature("Cars API")
@allure.story("Create car")
def test_create_car_success(api_url, unique_email, db_conn):
    """Позитивный тест: создание авто с проверкой сохранения в БД."""
    # Сначала создаём пользователя
    user_payload = {
        "email": unique_email,
        "name": "test_user",
        "password": "test_password",
    }
    user_resp = requests.post(f"{api_url}/users", json=user_payload)
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    car_payload = {
        "user_id": user_id,
        "brand": "Toyota",
        "model": "Camry",
        "year": 2022,
        "mileage": 15000,
    }

    with allure.step("Отправка POST запроса на создание авто"):
        allure.attach(
            body=json.dumps(car_payload, indent=2, default=str),
            name="Car payload",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/cars", json=car_payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2, default=str),
            name="Create response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 201
        car_id = resp.json()["id"]

    with allure.step("Проверка сохранения в БД"):
        row = db_conn.execute(
            "SELECT id, brand, model, year, mileage FROM cars WHERE id = %s", (car_id,)
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="Car DB row",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is not None
        assert row["brand"] == "Toyota"
        assert row["model"] == "Camry"


@allure.feature("Cars API")
@allure.story("Delete car")
def test_delete_car(api_url, unique_email, db_conn):
    """Позитивный тест: удаление авто с проверкой удаления из БД."""
    # Создаём пользователя и авто
    user_payload = {
        "email": unique_email,
        "name": "test_user",
        "password": "test_password",
    }
    user_resp = requests.post(f"{api_url}/users", json=user_payload)
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    car_payload = {
        "user_id": user_id,
        "brand": "Honda",
        "model": "Civic",
        "year": 2021,
        "mileage": 20000,
    }
    car_resp = requests.post(f"{api_url}/cars", json=car_payload)
    assert car_resp.status_code == 201
    car_id = str(car_resp.json()["id"])

    with allure.step("Проверка существования авто в БД"):
        row = db_conn.execute("SELECT id FROM cars WHERE id = %s", (car_id,)).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="Car before delete",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is not None

    with allure.step("Отправка DELETE запроса"):
        delete_url = f"{api_url}/cars/{car_id}"
        allure.attach(
            body=delete_url,
            name="Delete URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        delete_resp = requests.delete(delete_url)
        allure.attach(
            body=str(delete_resp.status_code),
            name="Delete status code",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert delete_resp.status_code == 204

    with allure.step("Проверка удаления из БД"):
        row = db_conn.execute("SELECT id FROM cars WHERE id = %s", (car_id,)).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="Car after delete",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is None


@allure.feature("Cars API")
@allure.story("Create car — user not found")
def test_create_car_user_not_found(api_url):
    """Негативный тест: создание авто с несуществующим user_id возвращает 404."""
    fake_user_id = uuid.uuid4()
    car_payload = {
        "user_id": str(fake_user_id),
        "brand": "BMW",
        "model": "X5",
        "year": 2023,
        "mileage": 0,
    }

    with allure.step("POST с несуществующим user_id"):
        allure.attach(
            body=json.dumps(car_payload, indent=2, default=str),
            name="Car payload (fake user)",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/cars", json=car_payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2, default=str),
            name="Not found response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 404


@allure.feature("Cars API")
@allure.story("Delete car — not found")
def test_delete_car_not_found(api_url):
    """Негативный тест: удаление несуществующего авто возвращает 404."""
    fake_car_id = uuid.uuid4()

    with allure.step("DELETE несуществующего авто"):
        delete_url = f"{api_url}/cars/{fake_car_id}"
        allure.attach(
            body=delete_url,
            name="Delete URL (fake ID)",
            attachment_type=allure.attachment_type.TEXT,
        )
        resp = requests.delete(delete_url)
        allure.attach(
            body=json.dumps(resp.json(), indent=2, default=str),
            name="Not found response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 404


@allure.feature("Cars API")
@allure.story("Get car — not found")
def test_get_car_not_found(api_url):
    """Негативный тест: получение несуществующего авто возвращает 404."""
    fake_car_id = uuid.uuid4()

    with allure.step("GET несуществующего авто"):
        get_url = f"{api_url}/cars/{fake_car_id}"
        allure.attach(
            body=get_url,
            name="Get URL (fake ID)",
            attachment_type=allure.attachment_type.TEXT,
        )
        resp = requests.get(get_url)
        allure.attach(
            body=json.dumps(resp.json(), indent=2, default=str),
            name="Not found response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 404

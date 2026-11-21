import json
import uuid

import allure
import requests


@allure.feature("Works API")
@allure.story("Create work")
def test_create_work_success(api_url, unique_email, db_conn):
    """Позитивный тест: создание записи о работе с проверкой сохранения в БД."""
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
    car_resp = requests.post(f"{api_url}/cars", json=car_payload)
    assert car_resp.status_code == 201
    car_id = car_resp.json()["id"]

    work_payload = {
        "car_id": car_id,
        "description": "Замена масла ДВС и фильтра",
        "mileage": 15000,
        "cost": 1500.0,
        "performed_date": "2024-06-15",
    }

    with allure.step("Отправка POST запроса на создание работы"):
        allure.attach(
            body=json.dumps(work_payload, indent=2, default=str),
            name="Work payload",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/works", json=work_payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2, default=str),
            name="Create response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 201
        work_id = resp.json()["id"]

    with allure.step("Проверка сохранения в БД"):
        row = db_conn.execute(
            "SELECT id, description, mileage, cost, performed_date FROM works WHERE id = %s",
            (work_id,),
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="Work DB row",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is not None
        assert row["description"] == "Замена масла ДВС и фильтра"
        assert row["cost"] == 1500.0


@allure.feature("Works API")
@allure.story("Delete work")
def test_delete_work(api_url, unique_email, db_conn):
    """Позитивный тест: удаление записи о работе с проверкой удаления из БД."""
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
    car_id = car_resp.json()["id"]

    work_payload = {
        "car_id": car_id,
        "description": "Замена передних тормозных колодок",
        "mileage": 20000,
        "cost": 5000.0,
        "performed_date": "2024-07-01",
    }
    work_resp = requests.post(f"{api_url}/works", json=work_payload)
    assert work_resp.status_code == 201
    work_id = str(work_resp.json()["id"])

    with allure.step("Проверка существования работы в БД"):
        row = db_conn.execute(
            "SELECT id FROM works WHERE id = %s", (work_id,)
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="Work before delete",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is not None

    with allure.step("Отправка DELETE запроса"):
        delete_url = f"{api_url}/works/{work_id}"
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
        row = db_conn.execute(
            "SELECT id FROM works WHERE id = %s", (work_id,)
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="Work after delete",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is None


@allure.feature("Works API")
@allure.story("Create work — car not found")
def test_create_work_car_not_found(api_url):
    """Негативный тест: создание работы с несуществующим car_id возвращает 404."""
    fake_car_id = uuid.uuid4()
    work_payload = {
        "car_id": str(fake_car_id),
        "description": "Замена воздушного фильтра",
        "mileage": 10000,
        "cost": 1500.0,
        "performed_date": "2024-06-15",
    }

    with allure.step("POST с несуществующим car_id"):
        allure.attach(
            body=json.dumps(work_payload, indent=2, default=str),
            name="Work payload (fake car)",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/works", json=work_payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2, default=str),
            name="Not found response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 404


@allure.feature("Works API")
@allure.story("Delete work — not found")
def test_delete_work_not_found(api_url):
    """Негативный тест: удаление несуществующей работы возвращает 404."""
    fake_work_id = uuid.uuid4()

    with allure.step("DELETE несуществующей работы"):
        delete_url = f"{api_url}/works/{fake_work_id}"
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


@allure.feature("Works API")
@allure.story("Get works by car")
def test_get_works_by_car(api_url, unique_email, db_conn):
    """Позитивный тест: получение списка работ для конкретного автомобиля."""
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
        "brand": "BMW",
        "model": "X5",
        "year": 2023,
        "mileage": 5000,
    }
    car_resp = requests.post(f"{api_url}/cars", json=car_payload)
    assert car_resp.status_code == 201
    car_id = car_resp.json()["id"]

    work_payload = {
        "car_id": car_id,
        "description": "Компьютерная диагностика двигателя",
        "mileage": 5000,
        "cost": 2000.0,
        "performed_date": "2024-08-01",
    }
    requests.post(f"{api_url}/works", json=work_payload)

    with allure.step("GET работ по авто"):
        get_url = f"{api_url}/works/car/{car_id}"
        allure.attach(
            body=get_url,
            name="Works by car URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        resp = requests.get(get_url)
        body = resp.json()
        allure.attach(
            body=json.dumps(body, indent=2, default=str),
            name="Works list",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 200
        assert len(body) >= 1
        assert body[0]["description"] == "Компьютерная диагностика двигателя"

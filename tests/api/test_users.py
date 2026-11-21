import json
import uuid

import allure
import requests

from app.backend.security import verify_password
from tests.api.helpers import assert_status, create_user


@allure.feature("Users API")
@allure.story("Create user")
def test_create_user_success(api_url, db_conn):
    """Позитивный тест: создание пользователя с проверкой хеширования пароля в БД."""
    payload = {
        "email": "test@test.com",
        "name": "test_user",
        "password": "test_password",
    }

    with allure.step("Отправка POST запроса на создание пользователя"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Post request",
            attachment_type=allure.attachment_type.JSON,
        )
        post_response = requests.post(f"{api_url}/users", json=payload)
        assert_status(post_response, 201)
        user_id = post_response.json()["id"]

    with allure.step("Проверка сохранения в базе данных"):
        row = db_conn.execute(
            "SELECT hashed_password FROM users WHERE id = %s", (user_id,)
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2),
            name="DB row",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is not None
        assert row["hashed_password"] != "test_password"

    with allure.step("Проверка хеширования пароля"):
        assert row["hashed_password"] is not None
        assert row["hashed_password"] != "test_password", (
            "password stored in plain text!"
        )
        assert verify_password("test_password", row["hashed_password"]) is True
        assert verify_password("wrong_password", row["hashed_password"]) is False


@allure.feature("Users API")
@allure.story("Delete user")
def test_delete_user(api_url, db_conn):
    """Позитивный тест: удаление пользователя с проверкой удаления из БД."""
    user = create_user(api_url)
    user_id = user["id"]

    with allure.step("Проверка существования пользователя в БД"):
        row = db_conn.execute(
            "SELECT id, email, name FROM users WHERE id = %s", (user_id,)
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="User before delete",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is not None

    with allure.step("Отправка DELETE запроса на удаление пользователя"):
        delete_url = f"{api_url}/users/{user_id}"
        allure.attach(
            body=delete_url,
            name="Delete URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        delete_response = requests.delete(delete_url)
        allure.attach(
            body=str(delete_response.status_code),
            name="Delete status code",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_status(delete_response, 204)

    with allure.step("Проверка удаления пользователя из БД"):
        row = db_conn.execute(
            "SELECT id FROM users WHERE id = %s", (user_id,)
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2, default=str),
            name="User after delete",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is None


# ─── Negative tests ────────────────────────────────────────────────────────


@allure.feature("Users API")
@allure.story("Create user — duplicate email")
def test_create_user_duplicate_email(api_url):
    """Негативный тест: создание пользователя с дублирующим email возвращает 409."""
    payload = {
        "email": "dup@test.com",
        "name": "test_user",
        "password": "test_password",
    }

    with allure.step("Создание первого пользователя"):
        first = requests.post(f"{api_url}/users", json=payload)
        assert_status(first, 201)

    with allure.step("Попытка создания второго пользователя с тем же email"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Duplicate payload",
            attachment_type=allure.attachment_type.JSON,
        )
        second = requests.post(f"{api_url}/users", json=payload)
        allure.attach(
            body=json.dumps(second.json(), indent=2),
            name="Conflict response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(second, 409)


@allure.feature("Users API")
@allure.story("Create user — missing password")
def test_create_user_missing_password(api_url):
    """Негативный тест: создание без password возвращает 422."""
    payload = {"email": f"no_pwd_{uuid.uuid4().hex[:8]}@test.com", "name": "test_user"}

    with allure.step("POST без password"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Missing password payload",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/users", json=payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2),
            name="Validation error",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 422)


@allure.feature("Users API")
@allure.story("Create user — missing name")
def test_create_user_missing_name(api_url):
    """Негативный тест: создание без name возвращает 422."""
    payload = {
        "email": f"no_name_{uuid.uuid4().hex[:8]}@test.com",
        "password": "test_password",
    }

    with allure.step("POST без name"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Missing name payload",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/users", json=payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2),
            name="Validation error",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 422)


@allure.feature("Users API")
@allure.story("Create user — invalid email")
def test_create_user_invalid_email(api_url):
    """Негативный тест: создание с невалидным email возвращает 422."""
    payload = {
        "email": "not-an-email",
        "name": "test_user",
        "password": "test_password",
    }

    with allure.step("POST с невалидным email"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Invalid email payload",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/users", json=payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2),
            name="Validation error",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 422)


@allure.feature("Users API")
@allure.story("Delete user — not found")
def test_delete_user_not_found(api_url):
    """Негативный тест: удаление несуществующего пользователя возвращает 404."""
    fake_id = uuid.uuid4()

    with allure.step("DELETE несуществующего пользователя"):
        delete_url = f"{api_url}/users/{fake_id}"
        allure.attach(
            body=delete_url,
            name="Delete URL (fake ID)",
            attachment_type=allure.attachment_type.TEXT,
        )
        resp = requests.delete(delete_url)
        allure.attach(
            body=json.dumps(resp.json(), indent=2),
            name="Not found response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 404)


@allure.feature("Users API")
@allure.story("Get user — not found")
def test_get_user_not_found(api_url):
    """Негативный тест: получение несуществующего пользователя возвращает 404."""
    fake_id = uuid.uuid4()

    with allure.step("GET несуществующего пользователя"):
        get_url = f"{api_url}/users/{fake_id}"
        allure.attach(
            body=get_url,
            name="Get URL (fake ID)",
            attachment_type=allure.attachment_type.TEXT,
        )
        resp = requests.get(get_url)
        allure.attach(
            body=json.dumps(resp.json(), indent=2),
            name="Not found response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 404)


@allure.feature("Users API")
@allure.story("Get users — non-empty list")
def test_get_users_non_empty(api_url):
    """Позитивный тест: GET списка после создания пользователя возвращает 200 + данные."""
    create_user(api_url)

    with allure.step("GET списка пользователей"):
        resp = requests.get(f"{api_url}/users")
        body = resp.json()
        allure.attach(
            body=json.dumps(body, indent=2, default=str),
            name="Users list",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 200)
        assert len(body) >= 1


@allure.feature("Users API")
@allure.story("Create user — empty fields")
def test_create_user_empty_fields(api_url):
    """Негативный тест: создание с пустыми полями возвращает 422."""
    payload = {"email": "", "name": "", "password": ""}

    with allure.step("POST с пустыми полями"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Empty fields payload",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/users", json=payload)
        allure.attach(
            body=json.dumps(resp.json(), indent=2),
            name="Validation error",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 422)


@allure.feature("Users API")
@allure.story("Create user — long fields")
def test_create_user_long_fields(api_url):
    """Граничный тест: создание с очень длинным name возвращает 422."""
    long_name = "A" * 500
    payload = {
        "email": f"long_{uuid.uuid4().hex[:8]}@test.com",
        "name": long_name,
        "password": "test_password",
    }

    with allure.step("POST с очень длинным name"):
        allure.attach(
            body=json.dumps({"name_length": len(long_name)}, indent=2),
            name="Long name payload summary",
            attachment_type=allure.attachment_type.JSON,
        )
        resp = requests.post(f"{api_url}/users", json=payload)
        try:
            body = resp.json()
        except requests.JSONDecodeError:
            body = resp.text
        allure.attach(
            body=json.dumps({"status": resp.status_code, "body": body}, indent=2),
            name="Response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert_status(resp, 422)

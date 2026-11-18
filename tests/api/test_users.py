import json
import uuid

import allure
import requests

from app.backend.security import verify_password


@allure.feature("Users API")
@allure.story("Create user")
def test_create_user_success(api_url, unique_email, db_conn):
    plain_password = "test_password"
    payload = {"email": unique_email, "name": "test_user", "password": plain_password}

    with allure.step("Отправка POST запроса на создание пользователя"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Post request",
            attachment_type=allure.attachment_type.JSON,
        )
        post_response = requests.post(f"{api_url}/users", json=payload)
        assert post_response.status_code == 201
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
        assert row["hashed_password"] != plain_password

    with allure.step("Проверка хеширования пароля"):
        assert row["hashed_password"] is not None
        assert row["hashed_password"] != plain_password, (
            "password stored in plain text!"
        )
        assert verify_password(plain_password, row["hashed_password"]) is True
        assert verify_password("wrong_password", row["hashed_password"]) is False


@allure.feature("Users API")
@allure.story("Delete user")
def test_delete_user(api_url, unique_email, db_conn):
    payload = {"email": unique_email, "name": "test_user", "password": "test_password"}

    with allure.step("Создание пользователя"):
        allure.attach(
            body=json.dumps(payload, indent=2),
            name="Request payload",
            attachment_type=allure.attachment_type.JSON,
        )
        create_response = requests.post(f"{api_url}/users", json=payload)
        create_json = create_response.json()
        user_id = str(create_json["id"])
        allure.attach(
            body=json.dumps(create_json, indent=2),
            name="Create response",
            attachment_type=allure.attachment_type.JSON,
        )
        assert create_response.status_code == 201

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
        assert delete_response.status_code == 204

    with allure.step("Проверка удаления пользователя из БД"):
        row = db_conn.execute(
            "SELECT id FROM users WHERE id = %s", (user_id,)
        ).fetchone()
        allure.attach(
            body=json.dumps(row, indent=2),
            name="User after delete",
            attachment_type=allure.attachment_type.JSON,
        )
        assert row is None


# ─── Negative tests ────────────────────────────────────────────────────────


@allure.feature("Users API")
@allure.story("Create user — duplicate email")
def test_create_user_duplicate_email(api_url, db_conn):
    email = f"dup_{uuid.uuid4().hex[:8]}@test.com"
    payload = {"email": email, "name": "test_user", "password": "test_password"}

    with allure.step("Создание первого пользователя"):
        first = requests.post(f"{api_url}/users", json=payload)
        assert first.status_code == 201

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
        assert second.status_code == 409


@allure.feature("Users API")
@allure.story("Create user — missing password")
def test_create_user_missing_password(api_url):
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
        assert resp.status_code == 422


@allure.feature("Users API")
@allure.story("Create user — missing name")
def test_create_user_missing_name(api_url):
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
        assert resp.status_code == 422


@allure.feature("Users API")
@allure.story("Create user — invalid email")
def test_create_user_invalid_email(api_url):
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
        assert resp.status_code == 422


@allure.feature("Users API")
@allure.story("Delete user — not found")
def test_delete_user_not_found(api_url):
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
        assert resp.status_code == 404


@allure.feature("Users API")
@allure.story("Get user — not found")
def test_get_user_not_found(api_url):
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
        assert resp.status_code == 404


# ─── Neutral / boundary tests ──────────────────────────────────────────────


@allure.feature("Users API")
@allure.story("Get users — empty list")
def test_get_users_empty(api_url):
    with allure.step("GET списка пользователей (пустая база)"):
        resp = requests.get(f"{api_url}/users")
        body = resp.json()
        allure.attach(
            body=json.dumps(body, indent=2),
            name="Empty users list",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 200
        assert body == []


@allure.feature("Users API")
@allure.story("Get users — non-empty list")
def test_get_users_non_empty(api_url, unique_email):
    payload = {"email": unique_email, "name": "test_user", "password": "test_password"}

    with allure.step("Создание пользователя для списка"):
        requests.post(f"{api_url}/users", json=payload)

    with allure.step("GET списка пользователей"):
        resp = requests.get(f"{api_url}/users")
        body = resp.json()
        allure.attach(
            body=json.dumps(body, indent=2),
            name="Users list",
            attachment_type=allure.attachment_type.JSON,
        )
        assert resp.status_code == 200
        assert len(body) >= 1


@allure.feature("Users API")
@allure.story("Create user — empty fields")
def test_create_user_empty_fields(api_url):
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
        assert resp.status_code == 422


@allure.feature("Users API")
@allure.story("Create user — long fields")
def test_create_user_long_fields(api_url):
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
        assert resp.status_code == 422

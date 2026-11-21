import os

import psycopg
import pytest
from psycopg.rows import dict_row

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://qa_sandbox_user:qa_sandbox_pass@127.0.0.1:5432/qa_sandbox_db",
)


@pytest.fixture(scope="session")
def api_url():
    return "http://127.0.0.1:8000/api/v1"


@pytest.fixture
def db_conn():
    with psycopg.connect(DB_URL, row_factory=dict_row) as conn:
        yield conn


@pytest.fixture(autouse=True)
def clean_db(db_conn):
    yield
    db_conn.execute("DELETE FROM works")
    db_conn.execute("DELETE FROM cars")
    db_conn.execute("DELETE FROM users")
    db_conn.commit()

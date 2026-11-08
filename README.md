# qa-sandbox



docker compose up -d
docker compose down -v

uv run alembic upgrade head
uv run alembic upgrade head
uv run alembic -x db=test upgrade head

uv run uvicorn main:app --reload

[Allure Report](https://veodev.github.io/qa-sandbox/builds/backend-tests/)
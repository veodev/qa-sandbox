# QA Sandbox 🚗

QA Sandbox — это полноценное Fullstack веб-приложение для учета автомобилей и работ по ним. Проект создан как полигон для отработки навыков ручного и автоматизированного тестирования (QA, QA Automation), а также демонстрации понимания Backend-разработки.

# Технологический стек
✅ Используется в проекте:
- **Backend:** *Python 3.14, Fastapi, Pydantic*
- **Database:** *PostgreSQL, SQLAlchemy, Alembic*
- **API Testing:** *Pytest, pytest-asyncio, httpx*
- **Infrastructure:** *Docker, GitHub Actions, Allure Reports, GitHub Pages, uv*

⏳ В процессе изучения и интеграции (Roadmap):
- **Frontend:** *HTML, CSS, Vanilla JS, Vue.js*
- **E2E Testing:** *Playwright*
- **AI Tools:** *Ollama, AI-Agents*

## Быстрый старт 🚀
### 1. Предварительные требования
- Убедитесь, что у вас установлены:
    - Docker и Docker Compose
    - uv (менеджер пакетов Python)
    - Make (для Windows: `winget install GnuWin32.Make`)
### 2. Клонирование и запуск
- git clone https://github.com/veodev/qa-sandbox.git
- cd qa-sandbox
- uv sync
- make up
- uv run uvicorn main:app --reload

docker compose up -d
docker compose down -v

uv run alembic upgrade head
uv run alembic upgrade head
uv run alembic -x db=test upgrade head

uv run uvicorn main:app --reload

[Allure Report](https://veodev.github.io/qa-sandbox/builds/backend-tests/)
# QA Sandbox 🚗

Демонстрационный стенд для отработки подходов к автоматизации тестирования.
Система учёта автомобилей и сервисного обслуживания (создание пользователей, авто, записей о работах).
Включает бэкенд (FastAPI, Uvicorn), базу данных (PostgreSQL) и фронтенд (JS, Nginx), упакованные в Docker.

🔗 **[Живой Allure-отчет](https://veodev.github.io/qa-sandbox/builds/backend-tests/)** | 📄 **[Swagger UI](http://localhost:8000/docs)** *(доступен после локального запуска)*

## 🛠 Технологический стек

| Категория | Инструменты |
| :--- | :--- |
| **Testing** | Python, Pytest, requests, Allure, psycopg |
| **Backend** | FastAPI, SQLAlchemy (async), Alembic |
| **Frontend** | HTML5, CSS3, Vanilla JS, Nginx |
| **Database** | PostgreSQL, asyncpg |
| **Infrastructure** | Docker, Docker Compose, Nginx |
| **CI/CD** | GitHub Actions, GitHub Pages |

## 🎯 Что внутри (Ключевые фишки)

*   **21 интеграционный тест:** Позитивные, негативные и граничные сценарии. Проверка каскадного удаления и связей сущностей.
*   **White Box проверки:** Тесты ходят напрямую в БД (через `psycopg`), чтобы проверять хеширование паролей и целостность данных, которые скрыты от API.
*   **Изоляция тестов:** Каждый тест запускается на чистой БД (фикстура с `TRUNCATE`), что исключает влияние тестов друг на друга.
*   **CI/CD:** Настроен пайплайн в GitHub Actions, который поднимает БД, накатывает миграции, запускает тесты и публикует Allure-отчет на GitHub Pages.
*   **AI-Assisted:** ИИ (GigaCode) использовался для генерации boilerplate-кода и фикстур.

## 🚀 Быстрый старт

Требования: Docker, `uv`, `make` (для Windows: `winget install GnuWin32.Make`, запускать в Git Bash).

```bash
# 1. Клонировать репозиторий
git clone https://github.com/veodev/qa-sandbox.git
cd qa-sandbox

# 2. Установить зависимости
uv sync

# 3. Поднять инфраструктуру (БД + Backend + Frontend)
make up

# 4. Запустить тесты и открыть отчет
make test
make report

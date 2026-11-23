.PHONY: help up down clean run-backend run-frontend db .check-docker .migrate .db

MAKEFLAGS += --no-print-directory

GREEN  := \033[0;32m
CYAN   := \033[0;36m
RED    := \033[0;31m
NC     := \033[0m

DOCKER_CHECK := $(shell docker info > /dev/null 2>&1 && echo OK)

# Usage: $(call print,text,color)
define print
	@echo -e "$(1)$(2)$(NC)"
endef

# Usage: $(call print_line,color,symbol(default='='),count(default=50))
define print_line
	@printf "$(1)%$(if $(3),$(3),50)s$(NC)\n" "" | tr " " "$(if $(2),$(2),=)"
endef

# Usage: $(call log_info,message,color) 
define log_info
	@echo -e "$(2)[Info] $(1)$(NC)"
endef

# Usage: $(call log_error,message) 
define log_error
	@echo -e "$(RED)[Error]$(1)$(NC)"
endef

# Usage: $(call print_success)
define print_success
	@$(call log_info,Done!,$(GREEN))
endef

define print_endpoints
	@$(call print_line,,#)
	@$(call log_info,Frontend\t\t: http://localhost,$(CYAN))
	@$(call log_info,Backend API\t: http://localhost:8000,$(CYAN))
	@$(call log_info,Swagger Docs\t: http://localhost:8000/docs,$(CYAN))
	@$(call log_info,PostgreSQL\t: http://localhost:5432,$(CYAN))
	@$(call print_line,,#)
endef

ifeq ($(OS),Windows_NT)
  ifndef MSYSTEM
    $(error [Error] Please run 'make' inside Git Bash!)
  endif
endif

.check-docker:
	@$(call log_info,Checking run docker...,$(CYAN))
ifneq ($(DOCKER_CHECK),OK)
	@$(call log_error,Docker is not running. Please start Docker Desktop.)
	@exit 1
endif

help:
	@$(call print_line)
	@$(call print,\tQA SANDBOX - AVAILABLE COMMANDS)
	@$(call print_line,,-)
	@$(call print,\t[DOCKER - Full Stand])
	@$(call print,make up\t\t\t: Build & start full stand (DB + Backend + Frontend))
	@$(call print,make down\t\t: Stop and remove containers)
	@$(call print,make clean\t\t: Stop and remove containers and volumes)
	@$(call print_line,,-)
	@$(call print,\t[LOCAL - Development])
	@$(call print,make db\t\t\t: Start DB only in Docker (stops Docker backend))
	@$(call print,make run-backend\t: Start local FastAPI server (with migrations))
	@$(call print,make run-frontend\t: Start local HTTP server)
	@$(call print,make migrate\t\t: Apply database migrations manually)
	@$(call print_line,,-)
	@$(call print,\t[QA - Testing & Reports])
	@$(call print,make test\t\t: Full test (API + UI))
	@$(call print,make test-api\t\t: Test API (Pytest))
	@$(call print,make test-ui\t\t: Test UI (Playwright))
	@$(call print,make report\t\t: Generate & view Allure report)
	@$(call print_line)

# Build & start full stand (DB + Backend + Frontend)
up: .check-docker
	@$(call log_info,Pull and build docker containers...,$(CYAN))
	@docker compose up -d --build --wait
	@$(call print_endpoints)
	@$(call print_success)

# Stop and remove containers
down: .check-docker
	@$(call log_info,Stop and remove containers...,$(CYAN))
	@docker compose down
	@$(call print_success)

# Stop and remove containers and volumes
clean: .check-docker
	@$(call log_info,Remove containers and volumes...,$(CYAN))
	@docker compose down -v
	@$(call print_success)

.db:
	@$(call log_info,Stop and remove "backend" container...,$(CYAN))
	@docker compose down backend
	@$(call log_info,Build and start "database" container...,$(CYAN))
	@docker compose up database -d --wait

# Start DB only in Docker (stops Docker backend)
db: .check-docker .db
	@$(call print_success)

# Start local FastAPI server (with migrations)
run-backend: .check-docker .db .migrate
	@uv run --directory app/backend uvicorn main:app --reload --port 8001 || true

run-frontend:
	@uv run --directory app/frontend python -m http.server 3000

.migrate:
	@$(call log_info,Apply database migrations...,$(CYAN))
	@uv run --directory app/backend alembic upgrade head

# Apply database migrations manually
migrate: .check-docker .migrate
	@$(call print_success)

test:
	@uv run pytest tests/api --alluredir=allure-results

# Generate & view Allure report
report:
	@echo "Generating Allure report..."
	@uv run pytest tests/ --alluredir=allure-results
	@allure serve allure-results || true


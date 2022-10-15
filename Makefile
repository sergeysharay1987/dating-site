RUN_MANAGE_PY = poetry run python manage.py

.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	${RUN_MANAGE_PY} migrate

.PHONY: migrations
migrations:
	${RUN_MANAGE_PY} makemigrations

.PHONY: update
update: install migrate ;

.PHONY: up-dependencies-only
up-dependencies-only:
	docker compose up --force-recreate db

.PHONY: run-server
run-server:
	${RUN_MANAGE_PY} runserver 127.0.0.1:8001

.PHONY: test
test:
	poetry run pytest

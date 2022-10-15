.PHONY: test
test:
	poetry run pytest

.PHONY: up-dependencies-only
up-dependencies-only:
	docker compose up --force-recreate db

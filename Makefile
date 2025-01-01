PHONY: install migrate migrations start_dev install-pre-commit lint superuser shell test update dev-db-up dev-db-down
install:
	poetry install --no-root

migrate:
	poetry run python -m src.manage migrate

migrations:
	poetry run python -m src.manage makemigrations

start_dev:
	poetry run python -m src.manage runserver

install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

lint:
	poetry run pre-commit run --all-files

superuser:
	poetry run python -m src.manage createsuperuser

shell:
	poetry run python -m src.manage shell

test:
	ls -lh && poetry run pytest -v --disable-warnings -rs -n auto --show-capture=no

test-dev:
	poetry run pytest -v -rs -n auto

update:
	install migrate

dev-up:
	test -f .env || touch .env
	docker compose -f docker-compose.dev.yml --project-name txt_sink_local_dev up -d

dev-down:
	docker compose -f docker-compose.dev.yml --project-name txt_sink_local_dev down

build:
	docker build -t cisco_test_project/txt-sink-api .

deploy:
	poetry run gunicorn src.core.asgi:application -k uvicorn_worker.UvicornWorker
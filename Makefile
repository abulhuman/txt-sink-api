PHONY: install migrate migrations runserver install-pre-commit lint superuser test update dev-db-up dev-db-down
install:
	poetry install

migrate:
	poetry run python -m src.manage migrate

migrations:
	poetry run python -m src.manage makemigrations

runserver:
	poetry run python -m src.manage runserver

install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

lint:
	poetry run pre-commit run --all-files

superuser:
	poetry run python -m src.manage createsuperuser

test:
	pytest -v --disable-warnings

update:
	install migrate

dev-db-up:
	test -f .env || touch .env
	docker compose -f docker-compose.dev.yaml --project-name txt_sink_dev_db up --force-recreate txt_sink_mysql -d

dev-db-down:
	docker compose -f docker-compose.dev.yaml --project-name txt_sink_dev_db down
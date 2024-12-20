PHONY: install migrate runserver superuser test update
install:
	poetry install

migrate:
	poetry run python -m src.manage migrate

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
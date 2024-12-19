PHONY: install migrate runserver superuser test update
install:
	poetry install

migrate:
	poetry run python -m src.manage migrate

runserver:
	poetry run python -m src.manage runserver

superuser:
	poetry run python -m src.manage createsuperuser

test:
	pytest -v --disable-warnings

update:
	install migrate
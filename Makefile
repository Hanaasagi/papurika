format:
	black papurika tests

lint:
	poetry run black --check --diff .
	poetry run flake8

test: lint
	poetry run pytest tests

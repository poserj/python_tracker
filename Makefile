run:
	uvicorn app.main:app --reload

format: ## Lint and static-chec
	isort .
	black --skip-string-normalization .
	mypy app/main.py

test:
	python3 -m unittest

setup:
	pip3 install poetry
	poetry install

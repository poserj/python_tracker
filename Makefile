run:
	uvicorn main:app --reload

format: ## Lint and static-chec
	isort .
	black --skip-string-normalization .
	mypy main.py

test: setup
	python3 -m unittest

setup:
	pip3 install poetry
	poetry install

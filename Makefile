run:
	uvicorn app.main:app --reload

format: ## Lint and static-chec
	isort .
	black --skip-string-normalization .
	mypy app/main.py

test:
	python3 -m unittest

setup:
	makdir build
	python -m venv dev
	source dev/bin/activate
	pip3 install poetry
	poetry install
table_create:
	python db/database.py



test1:
	python db/q1.py

db_up:
	sudo docker-compose up -d
	cd db && alembic upgrade head && cd ..

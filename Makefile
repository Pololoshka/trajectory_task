fix:
	ruff format src tests
	ruff check --fix --show-fixes src tests

check:
	ruff format --check src tests
	ruff check src tests
	mypy src tests
	pytest tests

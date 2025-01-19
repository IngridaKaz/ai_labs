.PHONY: check fix dev test test-cov

check:
	ruff check .
	@echo
	ruff format --check --diff

fix:
	ruff check --fix --show-fixes .
	@echo
	ruff format

dev:
	poetry install
	poetry shell
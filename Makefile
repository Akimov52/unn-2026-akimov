.PHONY: install test check build ruff-cs-check ruff-cs-fix ruff-linter-check ruff-linter-fix mypy-check

# Install development tools (Ruff and Mypy) into the uv environment.
install:
	uv sync --group dev

# Run the test suite.
test:
	uv run python -m unittest discover -s tests -v

# Run every check used by CI.
check: ruff-cs-check ruff-linter-check mypy-check test

# Ruff formatter: check / auto-fix.
ruff-cs-check:
	uv run ruff format --check .

ruff-cs-fix:
	uv run ruff format .

# Ruff linter: check / auto-fix.
ruff-linter-check:
	uv run ruff check .

ruff-linter-fix:
	uv run ruff check --fix .

# Static type checking.
mypy-check:
	uv run mypy

# Build the Docker image locally.
build:
	docker build -t unn-2026-akimov-bot-test .

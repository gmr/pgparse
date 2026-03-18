# List available recipes
default:
    @just --list

# Initialize submodules and sync dev dependencies
setup:
    git submodule update --init --recursive
    uv sync --group dev

# One-time local dev setup: sync deps and install pre-commit hooks
bootstrap: setup
    uv run pre-commit install --install-hooks

# Build libpg_query static library
build-libpg-query:
    make -C libpg_query

# Regenerate pgparse.c from pgparse.pyx (requires Cython in dev group)
generate: build-libpg-query
    uv run cython pgparse.pyx

# Build the extension and install in editable mode for testing
build-ext: build-libpg-query
    uv pip install --no-build-isolation --editable .

# Run tests with coverage
test: build-ext
    mkdir -p build
    uv run pytest --cov --cov-report=term-missing --cov-report=xml:build/coverage.xml

# Run linting and formatting checks
lint:
    uv run pre-commit run --all-files

# Build distribution wheels
build: build-libpg-query
    uv run python -m build --no-isolation

# Build documentation
docs:
    uv run mkdocs build --strict

# Serve documentation locally
docs-serve:
    uv run mkdocs serve

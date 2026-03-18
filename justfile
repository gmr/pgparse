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

# Regenerate pgparse.c from pgparse.pyx (requires Cython)
generate: build-libpg-query
    USE_CYTHON=1 uv run python setup.py build_ext --inplace

# Build the extension in-place for testing
build-ext: build-libpg-query
    uv run python setup.py build_ext --inplace

# Run tests with coverage
test: build-ext
    mkdir -p build
    uv run pytest --cov --cov-report=term-missing --cov-report=xml:build/coverage.xml

# Run linting and formatting checks
lint:
    uv run pre-commit run --all-files

# Build distribution wheels
build:
    USE_CYTHON=1 uv run python -m build

# Build documentation
docs:
    uv run mkdocs build --strict

# Serve documentation locally
docs-serve:
    uv run mkdocs serve

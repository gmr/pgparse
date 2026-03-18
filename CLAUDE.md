# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

`pgparse` is a thin Cython wrapper around [libpg_query](https://github.com/lfittl/libpg_query), which embeds PostgreSQL's parser as a standalone C library. The entire Python API lives in a single file, `pgparse.pyx`, which is transpiled to `pgparse.c` (committed to the repo) and compiled into a `.so` extension at build time.

- **`pgparse.pyx`** — Cython source; defines `parse()`, `normalize()`, `fingerprint()`, `parse_pgsql()`, and `PGQueryError`
- **`pgparse.c`** — pre-generated C file; built by Cython from `pgparse.pyx`; committed so the extension can be compiled without Cython installed
- **`libpg_query/`** — git submodule tracking the `17-latest` branch; provides `pg_query.h` and builds `libpg_query.a`

## Common Commands

```sh
just setup          # init submodule + uv sync --group dev (first time)
just bootstrap      # setup + install pre-commit hooks (one-time local dev)
just build-ext      # compile libpg_query + build pgparse.so in-place
just test           # build-ext then run pytest with coverage
just lint           # pre-commit run --all-files
just generate       # regenerate pgparse.c from pgparse.pyx (requires USE_CYTHON=1)
just build          # build distribution wheels
```

Run a single test file:
```sh
uv run pytest tests/test_parse.py
```

Run a single test method:
```sh
uv run pytest tests/test_parse.py::TestCase::test_happy_path
```

## Building the Extension

The extension must be compiled before tests can run. `just test` handles this automatically. To build manually:

```sh
make -C libpg_query                                  # build libpg_query.a first
uv pip install --no-build-isolation --editable .     # build and install the extension
```

The ext-module is configured in `[tool.setuptools]` in `pyproject.toml` and always builds from the pre-generated `pgparse.c`. To regenerate `pgparse.c` from `pgparse.pyx` (requires Cython in the dev group):

```sh
just generate
```

## libpg_query Submodule

The submodule tracks `origin/17-latest`. Postgres 18 support exists only on the upstream `18-latest-dev` branch (no stable release yet). To update:

```sh
git -C libpg_query fetch origin 17-latest
git -C libpg_query checkout origin/17-latest
```

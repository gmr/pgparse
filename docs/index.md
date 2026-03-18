# pgparse

Python bindings for [libpg_query](https://github.com/lfittl/libpg_query/), exposing PostgreSQL's internal parser to Python. Parse, normalize, and fingerprint SQL statements using the same parser that PostgreSQL itself uses.

[![Version](https://img.shields.io/pypi/v/pgparse.svg)](https://pypi.python.org/pypi/pgparse)
[![Coverage](https://codecov.io/gh/gmr/pgparse/branch/main/graph/badge.svg)](https://codecov.io/github/gmr/pgparse?branch=main)
[![License](https://img.shields.io/pypi/l/pgparse.svg)](https://github.com/gmr/pgparse/blob/main/LICENSE)

## PostgreSQL Compatibility

| pgparse | libpg_query | PostgreSQL |
|---------|-------------|------------|
| 1.x     | 17-latest   | 17         |

## Installation

```bash
pip install pgparse
```

Wheels are provided for Linux (manylinux and musllinux, x86_64 and aarch64) and macOS (arm64) for Python 3.11+ via the stable ABI (abi3). Installing from source requires `gcc`, `make`, and the libpg_query build dependencies.

## Usage

### Parse

Returns the internal PostgreSQL parse tree as a list of statement dicts:

```python
import pgparse

result = pgparse.parse("SELECT * FROM orders WHERE id = 1")
# [{'stmt': {'SelectStmt': {...}}}]
```

### Normalize

Replaces literal values with positional placeholders — useful for query grouping and log analysis:

```python
pgparse.normalize("SELECT * FROM orders WHERE id = 1")
# "SELECT * FROM orders WHERE id = $1"

pgparse.normalize("SELECT * FROM orders WHERE id = 2")
# "SELECT * FROM orders WHERE id = $1"
```

### Fingerprint

Produces a stable hash that is identical for structurally equivalent queries regardless of literal values or formatting:

```python
pgparse.fingerprint("SELECT * FROM orders WHERE id = 1")
# "0357e3db3ead2de761ea5c0f064bfddc0048cad5eb"

pgparse.fingerprint("SELECT * FROM orders WHERE id = 99")
# "0357e3db3ead2de761ea5c0f064bfddc0048cad5eb"  # same fingerprint
```

### Parse PL/pgSQL

Parse a PL/pgSQL function body:

```python
func = """
CREATE FUNCTION sales_tax(subtotal real) RETURNS real AS $$
    BEGIN
        RETURN subtotal * 0.06;
    END;
$$ LANGUAGE plpgsql;
"""
result = pgparse.parse_pgsql(func)
```

### Error Handling

Invalid SQL raises `pgparse.PGQueryError` with the error message and cursor position:

```python
try:
    pgparse.parse("SELECT FROM WHERE")
except pgparse.PGQueryError as e:
    print(e.message)   # syntax error at or near "WHERE"
    print(e.position)  # 13
```

## Further Reading

- [API Reference](api.md)
- [Examples](examples.md)
- [Version History](history.md)

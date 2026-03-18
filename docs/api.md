# API

The pgparse API is a direct wrapper of the functions provided by
[libpg_query](https://github.com/lfittl/libpg_query/).

## Functions

### pgparse.fingerprint(statement: str) -> str

::: pgparse.fingerprint

### pgparse.normalize(statement: str) -> str

::: pgparse.normalize

### pgparse.parse(statement: str) -> list

::: pgparse.parse

### pgparse.parse_pgsql(function: str) -> list

::: pgparse.parse_pgsql

## Exceptions

### pgparse.PGQueryError

::: pgparse.PGQueryError

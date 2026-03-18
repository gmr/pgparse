# pgparse

Python wrapper for [libpg_query](https://github.com/lfittl/libpg_query/)

[![Version](https://img.shields.io/pypi/v/pgparse.svg)](https://pypi.python.org/pypi/pgparse)
[![Coverage](https://codecov.io/gh/gmr/pgparse/branch/main/graph/badge.svg)](https://codecov.io/github/gmr/pgparse?branch=main)
[![License](https://img.shields.io/pypi/l/pgparse.svg)](https://github.com/gmr/pgparse/blob/main/LICENSE)
[![Docs](https://img.shields.io/readthedocs/pgparse.svg)](https://pgparse.readthedocs.io/)

## Installation

```bash
pip install pgparse
```

## Example Usage

The following example shows how to create a dump and then read it in, and
iterate through the data of one of the tables.

```python
import pprint

import pgparse

sql = "SELECT * FROM pg_catalog.pg_class WHERE relname = 'foo'"
print('Fingerprint: {}'.format(pgparse.fingerprint(sql)))
print('Normalized: {!r}'.format(pgparse.normalize(sql)))
parsed = pgparse.parse(sql)
pprint.pprint(parsed)

func = """\
CREATE FUNCTION sales_tax(subtotal real) RETURNS real AS $$
        BEGIN
            RETURN subtotal * 0.06;
        END;
        $$ LANGUAGE plpgsql;
"""
parsed = pgparse.parse_pgsql(func)
pprint.pprint(parsed)
```

## Documentation

- [API](api.md)
- [Examples](examples.md)
- [Version History](history.md)

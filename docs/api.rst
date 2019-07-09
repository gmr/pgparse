API
===
The pgparse API is a direct wrapper of the functions provided by
`libpg_query <https://github.com/lfittl/libpg_query/>`_.

Functions
---------
.. autofunction:: pgparse.fingerprint(statement: str) -> str
.. autofunction:: pgparse.normalize(statement: str) -> str
.. autofunction:: pgparse.parse(statement: str) -> list
.. autofunction:: pgparse.parse_pgsql(function: str) -> list

Exceptions
----------
.. autoexception:: pgparse.PGQueryError

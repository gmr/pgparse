# cython: language_level=3
"""
The pgparse API is a direct wrapper of the functions provided by
`libpg_query <https://github.com/lfittl/libpg_query/>`_.

"""
import json


cdef extern from "pg_query.h" nogil:

    int PG_VERSION_NUM

    ctypedef struct PgQueryError:
        char *message
        int cursorpos

    ctypedef struct PgQueryFingerprintResult:
        char *hexdigest
        PgQueryError *error

    ctypedef struct PgQueryNormalizeResult:
        char *normalized_query
        PgQueryError *error

    ctypedef struct PgQueryParseResult:
        char *parse_tree
        PgQueryError *error

    ctypedef struct PgQueryPlpgsqlParseResult:
        char *plpgsql_funcs
        PgQueryError *error

    PgQueryParseResult pg_query_parse(const char* input)
    PgQueryNormalizeResult pg_query_normalize(const char* input)
    PgQueryPlpgsqlParseResult pg_query_parse_plpgsql(const char* input)
    PgQueryFingerprintResult pg_query_fingerprint(const char* input)

    void pg_query_free_normalize_result(PgQueryNormalizeResult result)
    void pg_query_free_parse_result(PgQueryParseResult result)
    void pg_query_free_plpgsql_parse_result(PgQueryPlpgsqlParseResult result)
    void pg_query_free_fingerprint_result(PgQueryFingerprintResult result)


def fingerprint(statement: str) -> str:
    """Fingerprint a SQL statement

    Fingerprinting allows you to identify similar queries that are different
    only because of the specific object that is being queried for
    (i.e. different object ids in the WHERE clause), or because of formatting.

    :param str statement: The SQL statement to fingerprint
    :rtype: str
    :raises: :exc:`~pgparse.PGQueryError`

    """
    cdef PgQueryFingerprintResult result
    cdef bytes stmt

    stmt = statement.encode('UTF-8')
    result = pg_query_fingerprint(stmt)
    try:
        if result.error:
            raise PGQueryError(
                result.error.message.decode('utf-8'), result.error.cursorpos)
        return result.hexdigest.decode('UTF-8')
    finally:
        with nogil:
            pg_query_free_fingerprint_result(result)


def normalize(statement: str) -> str:
    """Normalize a SQL query, replacing values with placeholders

    :param str statement: The SQL statement to normalize
    :rtype: str
    :raises: :exc:`~pgparse.PGQueryError`

    """
    cdef PgQueryNormalizeResult result
    cdef bytes stmt

    stmt = statement.encode('UTF-8')
    result = pg_query_normalize(stmt)
    try:
        if result.error:
            raise PGQueryError(
                result.error.message.decode('utf-8'), result.error.cursorpos)
        return result.normalized_query.decode('UTF-8')
    finally:
        with nogil:
            pg_query_free_normalize_result(result)


def parse(statement: str) -> list:
    """Parse a SQL statement, returning a data structure that represents the
    internal PostgreSQL parse tree for the query.

    :param str statement: The SQL statement to parse
    :rtype: list
    :raises: :exc:`~pgparse.PGQueryError`

    """
    cdef PgQueryParseResult result
    cdef bytes stmt

    stmt = statement.encode('UTF-8')
    result = pg_query_parse(stmt)
    try:
        if result.error:
            raise PGQueryError(
                result.error.message.decode('utf-8'), result.error.cursorpos)
        return json.loads(result.parse_tree.decode('UTF-8'))
    finally:
        with nogil:
            pg_query_free_parse_result(result)



def parse_pgsql(function: str) -> list:
    """Parse a PL/PgSQL function, returning the internal PostgreSQL parse tree

    :param str function: The SQL function to parse
    :rtype: list
    :raises: :exc:`~pgparse.PGQueryError`

    """
    cdef PgQueryPlpgsqlParseResult result
    cdef bytes func

    func = function.encode('UTF-8')
    result = pg_query_parse_plpgsql(func)
    try:
        if result.error:
            raise PGQueryError(
                result.error.message.decode('utf-8'), result.error.cursorpos)
        return json.loads(result.plpgsql_funcs.decode('UTF-8'))
    finally:
        with nogil:
            pg_query_free_plpgsql_parse_result(result)


class PGQueryError(Exception):
    """Raised when invalid or unsupported SQL is parsed"""
    def __init__(self, message, position):
        self.message = message
        self.position = position

    def __str__(self):
        return '{} at position {}'.format(self.message, self.position)

# cython: language_level=3, linetrace=True, linetrace=True, linetrace=True
"""
The pgparse API is a direct wrapper of the functions provided by
`libpg_query <https://github.com/lfittl/libpg_query/>`_.

"""
import json
import typing
import pgparse_proto
from cpython.bytes cimport PyBytes_FromStringAndSize

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

    ctypedef struct PgQueryProtobuf:
        int len
        char *data

    ctypedef struct PgQueryProtobufParseResult:
        PgQueryProtobuf parse_tree
        char * stderr_buffer
        PgQueryError *error

    ctypedef struct PgQueryDeparseResult:
        char *query
        PgQueryError *error

    PgQueryParseResult pg_query_parse(const char* input)
    PgQueryNormalizeResult pg_query_normalize(const char* input)
    PgQueryPlpgsqlParseResult pg_query_parse_plpgsql(const char* input)
    PgQueryFingerprintResult pg_query_fingerprint(const char* input)
    PgQueryProtobufParseResult pg_query_parse_protobuf(const char* input)
    PgQueryDeparseResult pg_query_deparse_protobuf(PgQueryProtobuf parse_tree)

    void pg_query_free_normalize_result(PgQueryNormalizeResult result)
    void pg_query_free_parse_result(PgQueryParseResult result)
    void pg_query_free_plpgsql_parse_result(PgQueryPlpgsqlParseResult result)
    void pg_query_free_fingerprint_result(PgQueryFingerprintResult result)
    void pg_query_free_protobuf_parse_result(PgQueryProtobufParseResult result)
    void pg_query_free_deparse_result(PgQueryDeparseResult result)


def fingerprint(statement: str) -> str:
    """Fingerprint a SQL statement

    Fingerprinting allows you to identify similar queries that are different
    only because of the specific object that is being queried for
    (i.e. different object ids in the WHERE clause), or because of formatting.

    :param statement: The SQL statement to fingerprint
    :raises: :py:exc:`pgparse.PGQueryError`

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

    :param statement: The SQL statement to normalize
    :raises: :py:exc:`pgparse.PGQueryError`

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


def parse(statement: str) -> typing.List[typing.Dict]:
    """Parse a SQL statement, returning a data structure that represents the
    internal PostgreSQL parse tree for the query.

    :param statement: The SQL statement to parse
    :raises: :py:exc:`pgparse.PGQueryError`

    """
    cdef PgQueryParseResult result
    cdef bytes stmt

    stmt = statement.encode('UTF-8')
    result = pg_query_parse(stmt)
    try:
        if result.error:
            raise PGQueryError(
                result.error.message.decode('utf-8'), result.error.cursorpos)
        return json.loads(result.parse_tree.decode('UTF-8')).get('stmts', [])
    finally:
        with nogil:
            pg_query_free_parse_result(result)


def parse_pgsql(function: str) -> typing.List[typing.Dict]:
    """Parse a PL/PgSQL function, returning the internal PostgreSQL parse tree

    :param function: The SQL function to parse
    :raises: :py:exc:`pgparse.PGQueryError`

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


def parse_protobuf(statement: str) -> pgparse_proto.ParseResult:
    """Parse a SQL statement, returning a protobuf object

    :param statement: The SQL statement to parse
    :raises: :py:exc:`pgparse.PGQueryError`

    """
    cdef PgQueryProtobufParseResult result
    cdef bytes stmt

    stmt = statement.encode('UTF-8')
    result = pg_query_parse_protobuf(stmt)
    try:
        if result.error:
            raise PGQueryError(
                result.error.message.decode('utf-8'), result.error.cursorpos)
        pbbarray = PyBytes_FromStringAndSize(result.parse_tree.data, result.parse_tree.len)
        return pgparse_proto.ParseResult().FromString(pbbarray)
    finally:
            with nogil:
                pg_query_free_protobuf_parse_result(result)


def deparse_protobuf(parse_tree: pgparse_proto.ParseResult) -> str:
    """Deparse a protobuf object, returning an SQL statement

    :param parse_tree: Object to deparse
    :raises: :py:exc:`pgparse.PGQueryError`

    """
    cdef PgQueryDeparseResult result
    cdef PgQueryProtobuf serialized_parse_tree

    serialized_bytes = parse_tree.SerializeToString()
    serialized_parse_tree.data = serialized_bytes
    serialized_parse_tree.len = len(serialized_bytes)

    result = pg_query_deparse_protobuf(serialized_parse_tree)
    try:
        if result.error:
            raise PGQueryError(
                result.error.message.decode('utf-8'), result.error.cursorpos)
        return result.query.decode('utf-8')
    finally:
            with nogil:
                pg_query_free_deparse_result(result)


class PGQueryError(Exception):
    """Raised when invalid or unsupported SQL is parsed

    :var str message: The message provided by libpg_query
    :var int position: The position in the query for the error

    """
    def __init__(self, message, position):
        self.message = message
        self.position = position

    def __str__(self):
        return '{} at position {}'.format(self.message, self.position)

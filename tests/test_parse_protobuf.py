import unittest

from google.protobuf import json_format

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        expectation = {'version': 130002,
                       'stmts': [{
                           'stmt': {
                               'SelectStmt': {
                                   'targetList': [{
                                       'ResTarget': {
                                           'val': {
                                               'ColumnRef': {
                                                   'fields': [{
                                                       'A_Star': {}
                                                   }],
                                                   'location': 7
                                               }},
                                           'location': 7
                                       }}],
                                   'fromClause': [{
                                           'RangeVar': {
                                               'relname': 'foo',
                                               'inh': True,
                                               'relpersistence': 'p',
                                               'location': 14
                                           }}],
                                   'sortClause': [{
                                       'SortBy': {
                                           'node': {
                                               'ColumnRef': {
                                                   'fields': [{
                                                       'String': {
                                                           'str': 'bar'
                                                       }}],
                                                   'location': 27
                                               }},
                                           'sortby_dir': 'SORTBY_DEFAULT',
                                           'sortby_nulls':
                                               'SORTBY_NULLS_DEFAULT',
                                           'location': -1
                                       }}],
                                   'limitOption': 'LIMIT_OPTION_DEFAULT',
                                   'op': 'SETOP_NONE'
                               }}}]}
        result = pgparse.parse_protobuf('SELECT * FROM foo ORDER BY bar')
        self.assertDictEqual(json_format.MessageToDict(result), expectation)

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.parse_pgsql('FOO FROM BAR')

    def test_pgqueryerror_str_formatting(self):
        try:
            pgparse.parse_pgsql('FOO FROM BAR')
        except pgparse.PGQueryError as error:
            self.assertEqual(
                str(error), 'syntax error at or near "FOO" at position 1')

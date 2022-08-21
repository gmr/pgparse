import unittest

from google.protobuf import json_format
import pgparse_proto

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        expectation = 'SELECT * FROM foo ORDER BY bar'
        result = pgparse.deparse_protobuf(json_format.ParseDict(
            {'version': 130002,
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
                     }}}]},
            pgparse_proto.ParseResult()
        ))
        self.assertEqual(result, expectation)

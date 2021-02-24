import unittest

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        expectation = {
            'stmt': {
                'SelectStmt': {
                    'fromClause': [{
                        'RangeVar': {
                            'inh': True,
                            'location': 14,
                            'relname': 'foo',
                            'relpersistence': 'p'
                        }
                    }],
                    'limitOption': 'LIMIT_OPTION_DEFAULT',
                    'op': 'SETOP_NONE',
                    'sortClause': [{
                        'SortBy': {
                            'location': -1,
                            'node': {
                                'ColumnRef': {
                                    'fields': [{
                                        'String': {
                                            'str': 'bar'
                                        }
                                    }],
                                    'location': 27
                                }
                            },
                            'sortby_dir': 'SORTBY_DEFAULT',
                            'sortby_nulls': 'SORTBY_NULLS_DEFAULT'
                        }
                    }],
                    'targetList': [{
                        'ResTarget': {
                            'location': 7,
                            'val': {
                                'ColumnRef': {
                                    'fields': [{
                                        'A_Star': {}
                                    }],
                                    'location': 7
                                }
                            }
                        }
                    }]
                }
            }
        }
        result = pgparse.parse('SELECT * FROM foo ORDER BY bar')
        self.assertEqual(len(result), 1)
        self.assertDictEqual(result[0], expectation)

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.parse_pgsql('FOO FROM BAR')

    def test_pgqueryerror_str_formatting(self):
        try:
            pgparse.parse_pgsql('FOO FROM BAR')
        except pgparse.PGQueryError as error:
            self.assertEqual(
                str(error), 'syntax error at or near "FOO" at position 1')

import unittest

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        result = pgparse.parse('SELECT * FROM foo ORDER BY bar')
        expectation = [{
            'RawStmt': {
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
                        'op':
                        0,
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
                                'sortby_dir': 0,
                                'sortby_nulls': 0
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
        }]
        for offset in range(0, len(expectation)):
            self.assertDictEqual(result[offset], expectation[0])

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.parse_pgsql('FOO FROM BAR')

    def test_pgqueryerror_str_formatting(self):
        try:
            pgparse.parse_pgsql('FOO FROM BAR')
        except pgparse.PGQueryError as error:
            self.assertEqual(
                str(error), 'syntax error at or near "FOO" at position 1')

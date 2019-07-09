import unittest

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        definition = """\
            CREATE FUNCTION sales_tax(subtotal real) RETURNS real AS $$
            BEGIN
                RETURN subtotal * 0.06;
            END;
            $$ LANGUAGE plpgsql;"""
        result = pgparse.parse_pgsql(definition)
        expectation = [{
            'PLpgSQL_function': {
                'action': {
                    'PLpgSQL_stmt_block': {
                        'body': [{
                            'PLpgSQL_stmt_return': {
                                'expr': {
                                    'PLpgSQL_expr': {
                                        'query': 'SELECT '
                                        'subtotal '
                                        '* '
                                        '0.06'
                                    }
                                },
                                'lineno': 3
                            }
                        }],
                        'lineno':
                        2
                    }
                },
                'datums': [{
                    'PLpgSQL_var': {
                        'datatype': {
                            'PLpgSQL_type': {
                                'typname': 'UNKNOWN'
                            }
                        },
                        'refname': 'found'
                    }
                }]
            }
        }]
        for offset in range(0, len(expectation)):
            self.assertDictEqual(result[offset], expectation[0])

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.parse('FOO FROM BAR')

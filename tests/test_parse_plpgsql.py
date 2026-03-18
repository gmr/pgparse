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
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        func = result[0].get('PLpgSQL_function', {})
        self.assertIn('action', func)
        self.assertIn('datums', func)
        # The function should have the subtotal parameter and found in datums
        datums = func['datums']
        refnames = [d.get('PLpgSQL_var', {}).get('refname') for d in datums]
        self.assertIn('found', refnames)
        self.assertIn('subtotal', refnames)
        # The action should contain a RETURN statement
        action = func['action']
        self.assertIn('PLpgSQL_stmt_block', action)
        body = action['PLpgSQL_stmt_block']['body']
        self.assertEqual(len(body), 1)
        stmt = body[0]
        self.assertIn('PLpgSQL_stmt_return', stmt)
        expr = stmt['PLpgSQL_stmt_return']['expr']['PLpgSQL_expr']
        self.assertIn('subtotal', expr['query'])
        self.assertIn('0.06', expr['query'])

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.parse('FOO FROM BAR')

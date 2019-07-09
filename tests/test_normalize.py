import unittest

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        expectation = 'SELECT * FROM foo WHERE x = $1'
        self.assertEqual(pgparse.normalize('SELECT * FROM foo WHERE x = 1'),
                         expectation)
        self.assertEqual(pgparse.normalize('SELECT * FROM foo WHERE x = 2'),
                         expectation)

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.normalize('FOO FROM BAR')

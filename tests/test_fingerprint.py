import unittest

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        expectation = '38af4ccdfef2d9b2'
        self.assertEqual(
            pgparse.fingerprint('SELECT * FROM foo WHERE x = 1'), expectation
        )
        self.assertEqual(
            pgparse.fingerprint('SELECT * FROM foo WHERE x = 2'), expectation
        )

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.fingerprint('FOO FROM BAR')

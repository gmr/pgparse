import unittest

import pgparse


class TestCase(unittest.TestCase):
    def test_happy_path(self):
        expectation = '0357e3db3ead2de761ea5c0f064bfddc0048cad5eb'
        self.assertEqual(pgparse.fingerprint('SELECT * FROM foo WHERE x = 1'),
                         expectation)
        self.assertEqual(pgparse.fingerprint('SELECT * FROM foo WHERE x = 2'),
                         expectation)

    def test_invalid_sql_raises(self):
        with self.assertRaises(pgparse.PGQueryError):
            pgparse.fingerprint('FOO FROM BAR')

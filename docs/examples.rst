Examples
========
The following snippet demonstrates how to get a query fingerprint, return a
normalized query, parse SQL, and parse a PL/PgSQL function.

.. code:: python

    import pprint

    import pgparse

    sql = "SELECT * FROM pg_catalog.pg_class WHERE relname = 'foo'"
    print('Fingerprint: {}'.format(pgparse.fingerprint(sql)))
    print('Normalized: {!r}'.format(pgparse.normalize(sql)))
    parsed = pgparse.parse(sql)
    pprint.pprint(parsed)

    func = """\
    CREATE FUNCTION sales_tax(subtotal real) RETURNS real AS $$
            BEGIN
                RETURN subtotal * 0.06;
            END;
            $$ LANGUAGE plpgsql;
    """
    parsed = pgparse.parse_pgsql(func)
    pprint.pprint(parsed)

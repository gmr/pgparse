pgparse
=======

Python wrapper for `libpg_query <https://github.com/lfittl/libpg_query/>`_

|Version| |Status| |Coverage| |License| |Docs|

Installation
------------

.. code-block:: bash

    pip install pgparse

Example Usage
-------------

The following example shows how to create a dump and then read it in, and
iterate through the data of one of the tables.

.. code-block:: python

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


.. |Version| image:: https://img.shields.io/pypi/v/pgparse.svg?
   :target: https://pypi.python.org/pypi/pgparse
   :alt: Package Version

.. |Status| image:: https://img.shields.io/circleci/build/gh/gmr/pgparse/master.svg?token=3d274067c09738c1ce3a77650138ee9cc9614cdb
   :target: https://circleci.com/gh/gmr/pgparse/tree/master
   :alt: Build Status

.. |Coverage| image:: https://codecov.io/gh/gmr/pgparse/branch/master/graph/badge.svg
   :target: https://codecov.io/github/gmr/pgparse?branch=master
   :alt: Code Coverage

.. |License| image:: https://img.shields.io/pypi/l/pgparse.svg?
   :target: https://github.com/gmr/pgparse/blob/master/LICENSE
   :alt: BSD

.. |Docs| image:: https://img.shields.io/readthedocs/pgparse.svg?
   :target: https://pgparse.readthedocs.io/
   :alt: Documentation Status



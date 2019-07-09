#!/usr/bin/env sh
set -e
sed -i.bak 's/# cython: language_level=3/# cython: language_level=3, linetrace=True/' pgparse.pyx
rm -f pgparse.pyx.bak
USE_CYTHON=1 python setup.py build_ext -i --define CYTHON_TRACE_NOGIL
flake8 --output build/flake8.txt --tee
coverage run setup.py nosetests
coverage report -m pgparse.pyx
coverage xml -o build/coverage.xml pgparse.pyx
git checkout pgparse.pyx pgparse.c

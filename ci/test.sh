#!/usr/bin/env sh
set -e
TEST_BUILD=1 USE_CYTHON=1 python setup.py build_ext -i --define CYTHON_TRACE_NOGIL
flake8 --output build/flake8.txt --tee
coverage run setup.py nosetests
coverage report -m pgparse.pyx
coverage xml -o build/coverage.xml pgparse.pyx

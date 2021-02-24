#!/usr/bin/env sh
set -e
mkdir -p build
flake8 --output build/flake8.txt --tee
USE_CYTHON=1 python3 setup.py build_ext --force --inplace --define CYTHON_TRACE_NOGIL
coverage run setup.py nosetests
coverage report -m pgparse.pyx
coverage xml -o build/coverage.xml pgparse.pyx

#!/usr/bin/env python3
import os
import pathlib
import subprocess
import sys

import setuptools
from setuptools.command import build_ext

if bool(os.environ.get('USE_CYTHON')):
    from Cython.Build import cythonize
else:
    cythonize = None

LIBPG_QUERY = str(pathlib.Path('./libpg_query'))


class BuildExt(build_ext.build_ext):
    def run(self):
        return_code = subprocess.call(['make', '-C', LIBPG_QUERY, 'build'])
        if return_code:
            sys.stderr.write('libpg_query failed to build')
            sys.exit(return_code)
        super().run()


ext_modules = [
    setuptools.Extension(
        'pgparse',
        ['pgparse.c' if cythonize is None else 'pgparse.pyx'],
        libraries=['pg_query'],
        include_dirs=[LIBPG_QUERY],
        library_dirs=[LIBPG_QUERY])]

setuptools.setup(
    cmdclass={'build_ext': BuildExt},
    ext_modules=ext_modules if cythonize is None else
    cythonize(ext_modules))

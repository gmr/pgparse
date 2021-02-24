#!/usr/bin/env python3
import os
import subprocess
import sys
import sysconfig

import setuptools
from setuptools.command import build_ext
if os.environ.get('USE_CYTHON') in ['1', 'true', 'TRUE', 'Y']:
    from Cython.Build import cythonize
else:
    cythonize = None

LIBPG_QUERY = './libpg_query'
LIBRARIES = ['pg_query']
if 'musl' in sysconfig.get_config_var('BUILD_GNU_TYPE'):
    LIBRARIES.append('execinfo')

EXT_MODULES = [
        setuptools.Extension(
            'pgparse',
            ['pgparse.c' if cythonize is None else 'pgparse.pyx'],
            libraries=LIBRARIES,
            include_dirs=[LIBPG_QUERY],
            library_dirs=[LIBPG_QUERY])]


class BuildExt(build_ext.build_ext):
    def run(self):
        return_code = subprocess.call(
            ['make', '-C', LIBPG_QUERY, 'build'])
        if return_code:
            sys.stderr.write('libpg_query failed to build')
            sys.exit(return_code)
        super().run()


setuptools.setup(
    cmdclass={'build_ext': BuildExt},
    ext_modules=EXT_MODULES if cythonize is None else cythonize(EXT_MODULES),
    zip_safe=False)

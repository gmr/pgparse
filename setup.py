#!/usr/bin/env python3
import os
import subprocess
import sys
import sysconfig

import setuptools
from setuptools.command import build_ext
import setuptools.command.build_py

if os.environ.get('USE_CYTHON') in ['1', 'true', 'TRUE', 'Y']:
    from Cython.Build import cythonize
else:
    cythonize = None

if os.environ.get('USE_PROTOC') in ['1', 'true', 'TRUE', 'Y']:
    protoc = 'protoc'
else:
    protoc = None

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


class BuildPyCommand(setuptools.command.build_py.build_py):
    def run(self):
        if protoc:
            return_code = subprocess.call(
                [protoc, '-I', f'{LIBPG_QUERY}/protobuf', '--python_out', '.',
                 f'{LIBPG_QUERY}/protobuf/pg_query.proto'])
            if return_code:
                sys.stderr.write('Failed to run protoc')
                sys.exit(return_code)
            os.rename('pg_query_pb2.py', 'pgparse_proto.py')
        setuptools.command.build_py.build_py.run(self)


setuptools.setup(
    cmdclass={'build_ext': BuildExt,
              'build_py': BuildPyCommand},
    py_modules=['pgparse_proto'],
    ext_modules=EXT_MODULES if cythonize is None else cythonize(EXT_MODULES),
    zip_safe=False)

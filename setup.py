import os
import pathlib
import subprocess
import sysconfig

import setuptools
import setuptools.command.build_ext

LIBPG_QUERY = 'libpg_query'

libraries = ['pg_query']
if 'musl' in sysconfig.get_config_var('BUILD_GNU_TYPE'):
    import ctypes.util
    if ctypes.util.find_library('execinfo'):
        libraries.append('execinfo')


class BuildExt(setuptools.command.build_ext.build_ext):
    """Custom build_ext that ensures libpg_query is compiled first."""

    def run(self):
        libpg_query_dir = pathlib.Path(__file__).parent / LIBPG_QUERY
        if not (libpg_query_dir / 'libpg_query.a').exists():
            subprocess.run(  # noqa: S603
                ['make', '-C', str(libpg_query_dir), 'build'],  # noqa: S607
                check=True,
            )
        super().run()


sources = ['pgparse.pyx'] if os.getenv('USE_CYTHON') else ['pgparse.c']

ext = setuptools.Extension(
    'pgparse',
    sources=sources,
    include_dirs=[LIBPG_QUERY],
    library_dirs=[LIBPG_QUERY],
    libraries=libraries,
    define_macros=[('CYTHON_TRACE', '1')],
)

if os.getenv('USE_CYTHON'):
    import Cython.Build

    ext_modules = Cython.Build.cythonize(
        [ext],
        compiler_directives={
            'language_level': '3',
            'linetrace': True,
        },
    )
else:
    ext_modules = [ext]

setuptools.setup(
    cmdclass={'build_ext': BuildExt},
    ext_modules=ext_modules,
)

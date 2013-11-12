import sys
import os
from subprocess import Popen

from itertools import chain

from pkg_resources import require
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

REQUIRES = open('requirements.txt').read().strip().split('\n')

VERSION = open('VERSION').read().strip()

PACKAGE_DIR = '.'
# Also gets the header files if building an egg
PACKAGE_DATA = ['VERSION', 'requirements.txt']

# Gets the header files for installing to sys.prefix
# if doing normal build/install
DATA_FILES = []

# Create data file lists if some build/install cmd was given
if any(cmd in sys.argv for cmd in ('build', 'install', 'bdist_egg')):
    require(REQUIRES)

    from path import path as Path

    PACKAGE_DIR = Path(PACKAGE_DIR)

    if not 'bdist_egg' in sys.argv:
        PREFIX = Path(sys.prefix).abspath()
        # Store sys.prefix location (where data_files are installed)
        # as part of package_data.
        # Can later be accessed with libcarefree_objects.PREFIX
        with open('PREFIX', 'w') as f:
            f.write(PREFIX)
        PACKAGE_DATA.append('PREFIX')

    INCLUDE_FILES = []
    with Path('include'):
        for dirpath, dirnames, filenames in os.walk('.'):
            abspath = Path(dirpath).abspath()
            filepaths = []
            for fn in filenames:
                if Path(fn).ext == '.hpp':
                    filepaths.append(abspath.joinpath(fn))
            if filepaths:
                INCLUDE_FILES.append((dirpath, filepaths))

    if not 'bdist_egg' in sys.argv:
        # Install headers as data_files to sys.prefix
        for dirpath, filepaths in INCLUDE_FILES:
            DATA_FILES.append(
              (PREFIX.joinpath('include', dirpath), filepaths))
    else:
        # Install headers as package_data
        for dirpath, filepaths in INCLUDE_FILES:
            for path in filepaths:
                PACKAGE_DATA.append(PACKAGE_DIR.relpathto(path))

setup(
  name='libarray_ptr',
  version=VERSION,
  description=(
    "A simple C-style-array ptr/size wrapper template for C++"
    " with STL container functionality"
    " and support for std::vector and std::array"
    ),
  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',

  url='http://bitbucket.org/StefanZimmermann/array_ptr',

  license='LGPLv3',

  install_requires=REQUIRES,

  package_dir={
    'libarray_ptr': PACKAGE_DIR,
    },
  packages=[
    'libarray_ptr',
    ],
  package_data={
    'libarray_ptr': PACKAGE_DATA,
    },

  data_files=DATA_FILES,
  )

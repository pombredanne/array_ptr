import sys
import os
from distutils.core import setup

REQUIRES = [
  'path.py',
  ]

VERSION = open('VERSION').read().strip()

DATA_FILES = []

if any(cmd in sys.argv for cmd in ('build', 'install')):
    from path import path as Path

    PREFIX = Path(sys.prefix).abspath()

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

    DATA_FILES.extend(
      (PREFIX.joinpath('include', dirpath), filenames)
      for dirpath, filenames in INCLUDE_FILES)

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

  setup_requires=REQUIRES,

  data_files=DATA_FILES,
  )

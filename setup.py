import sys
import os

from itertools import chain

from distutils.core import setup

# The setup_requires list
REQUIRES = [
  'path.py',
  ]
# pip uses setuptools uses easy_install
# for installing setup_requires packages,
# which are bdist_egg'd and installed to ./*.egg/ dirs...
for name in os.listdir('.'):
    if name.endswith('.egg'):
        path = os.path.abspath(name)
        sys.path.insert(0, path)
        try:
            PYTHONPATH = os.pathsep.join((path, os.environ['PYTHONPATH']))
        except KeyError:
            PYTHONPATH = path
        os.environ['PYTHONPATH'] = PYTHONPATH

VERSION = open('VERSION').read().strip()

PACKAGE_DIR = '.'
# Gets the header files if building an egg
PACKAGE_DATA = []

# Gets the header files for installing to sys.prefix
# if doing normal build/install
DATA_FILES = []

# Create data file lists if some build/install cmd was given
if any(cmd in sys.argv for cmd in ('build', 'install', 'bdist_egg')):
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

  setup_requires=REQUIRES,
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

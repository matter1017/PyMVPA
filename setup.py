#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Python distutils setup for PyMVPA"""

from numpy.distutils.core import setup, Extension
import os
import sys
from glob import glob

# some config settings
bind_libsvm = 'local' # choices: 'local', 'system', None

libsvmc_extra_sources = []
libsvmc_include_dirs = []
libsvmc_libraries = []

extra_link_args = []
libsvmc_library_dirs = []

# platform-specific settings
if sys.platform == "darwin":
    extra_link_args.append("-bundle")

if sys.platform.startswith('linux'):
    # need to look for numpy (header location changes with v1.3)
    libsvmc_include_dirs += ['/usr/include/numpy']

# when libsvm is forced -- before it was used only in cases
# when libsvm was available at system level, hence we switch
# from local to system at this point
# TODO: Deprecate --with-libsvm for 0.5
for arg in ('--with-libsvm', '--with-system-libsvm'):
    if not sys.argv.count(arg):
        continue
    # clean argv if necessary (or distutils will complain)
    sys.argv.remove(arg)
    # assure since default is 'auto' wouldn't fail if it is N/A
    bind_libsvm = 'system'

# when no libsvm bindings are requested explicitly
if sys.argv.count('--no-libsvm'):
    # clean argv if necessary (or distutils will complain)
    sys.argv.remove('--no-libsvm')
    bind_libsvm = None

# if requested:
if bind_libsvm == 'local':
    # we will provide libsvm sources later on # if libsvm.a is available locally -- use it
    #if os.path.exists(os.path.join('build', 'libsvm', 'libsvm.a')):
    libsvm_3rd_path = os.path.join('3rd', 'libsvm')
    libsvmc_include_dirs += [libsvm_3rd_path]
    libsvmc_extra_sources = [os.path.join(libsvm_3rd_path, 'svm.cpp')]
elif bind_libsvm == 'system':
    # look for libsvm in some places, when local one is not used
    libsvmc_libraries += ['svm']
    if not sys.platform.startswith('win'):
        libsvmc_include_dirs += [
            '/usr/include/libsvm-3.0/libsvm',
            '/usr/include/libsvm-2.0/libsvm',
            '/usr/include/libsvm',
            '/usr/local/include/libsvm',
            '/usr/local/include/libsvm-2.0/libsvm',
            '/usr/local/include']
    else:
        # no clue on windows
        pass
elif bind_libsvm is None:
    pass
else:
    raise ValueError("Shouldn't happen that we get bind_libsvm=%r"
                     % (bind_libsvm,))


# define the extension modules
libsvmc_ext = Extension(
    'mvpa2.clfs.libsvmc._svmc',
    sources = libsvmc_extra_sources + ['mvpa2/clfs/libsvmc/svmc.i'],
    include_dirs = libsvmc_include_dirs,
    library_dirs = libsvmc_library_dirs,
    libraries    = libsvmc_libraries,
    language     = 'c++',
    extra_link_args = extra_link_args,
    swig_opts    = ['-I' + d for d in libsvmc_include_dirs])

smlrc_ext = Extension(
    'mvpa2.clfs.libsmlrc.smlrc',
    sources = [ 'mvpa2/clfs/libsmlrc/smlr.c' ],
    #library_dirs = library_dirs,
    libraries = ['m'],
    # extra_compile_args = ['-O0'],
    extra_link_args = extra_link_args,
    language = 'c')

ext_modules = [smlrc_ext]

if bind_libsvm:
    ext_modules.append(libsvmc_ext)

# Notes on the setup
# Version scheme is: major.minor.patch<suffix>

# define the setup
setup(name         = 'pymvpa2',
      version      = '2.1.0',
      author       = 'Michael Hanke, Yaroslav Halchenko, Per B. Sederberg',
      author_email = 'pkg-exppsy-pymvpa@lists.alioth.debian.org',
      license      = 'MIT License',
      url          = 'http://www.pymvpa.org',
      description  = 'Multivariate pattern analysis',
      long_description = \
          "PyMVPA is a Python module intended to ease pattern classification " \
          "analyses of large datasets. It provides high-level abstraction of " \
          "typical processing steps and a number of implementations of some " \
          "popular algorithms. While it is not limited to neuroimaging data " \
          "it is eminently suited for such datasets.\n" \
          "PyMVPA is truly free software (in every respect) and " \
          "additionally requires nothing but free-software to run.",
      # please maintain alphanumeric order
      packages     = [ 'mvpa2',
                       'mvpa2.algorithms',
                       'mvpa2.atlases',
                       'mvpa2.base',
                       'mvpa2.clfs',
                       'mvpa2.clfs.libsmlrc',
                       'mvpa2.clfs.libsvmc',
                       'mvpa2.clfs.skl',
                       'mvpa2.clfs.sg',
                       'mvpa2.datasets',
                       'mvpa2.featsel',
                       'mvpa2.kernels',
                       'mvpa2.mappers',
                       'mvpa2.generators',
                       'mvpa2.measures',
                       'mvpa2.misc',
                       'mvpa2.misc.bv',
                       'mvpa2.misc.fsl',
                       'mvpa2.misc.io',
                       'mvpa2.misc.plot',
                       'mvpa2.support',
                       'mvpa2.support.bayes',
                       'mvpa2.support.nipy',
                       'mvpa2.support.ipython',
                       'mvpa2.testing',
                       'mvpa2.tests',
                       'mvpa2.tests.badexternals',
                       ],
      data_files = [('mvpa2', ['mvpa2/COMMIT_HASH']),
                    ('mvpa2/data',
                     [f for f in glob(os.path.join('mvpa2', 'data', '*'))
                         if os.path.isfile(f)]),
                    ('mvpa2/data/bv',
                     [f for f in glob(os.path.join('mvpa2', 'data', 'bv', '*'))
                         if os.path.isfile(f)])],
      scripts      = glob(os.path.join('bin', '*')),
      ext_modules  = ext_modules
      )


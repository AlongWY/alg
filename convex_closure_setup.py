# distutils: language=3
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('convex_closure_opt.pyx', language=3))

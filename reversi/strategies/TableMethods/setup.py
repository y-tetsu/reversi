from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


# GetScoreFast
ext_modules = [Extension("GetScoreFast", ["GetScoreFast.pyx"])]

setup(
    name='GetScoreFast',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

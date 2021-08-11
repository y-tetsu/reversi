from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


# EvaluateFast
ext_modules = [Extension("EvaluateFast", ["EvaluateFast.pyx"])]

setup(
    name='EvaluateFast',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

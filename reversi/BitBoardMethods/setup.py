from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# GetPsossiblesFast
ext_modules = [Extension("GetLegalMovesFast", ["GetLegalMovesFast.pyx"])]

setup(
  name = 'GetLegalMovesFast',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

# GetBoardInfoFast
ext_modules = [Extension("GetBoardInfoFast", ["GetBoardInfoFast.pyx"])]

setup(
  name = 'GetBoardInfoFast',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

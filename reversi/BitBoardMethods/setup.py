from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# GetLegalMovesFast
ext_modules = [Extension("GetLegalMovesFast", ["GetLegalMovesFast.pyx"])]

setup(
    name='GetLegalMovesFast',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

# GetFlippableDiscsFast
ext_modules = [Extension("GetFlippableDiscsFast", ["GetFlippableDiscsFast.pyx"])]

setup(
    name='GetFlippableDiscsFast',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

# GetBoardInfoFast
ext_modules = [Extension("GetBoardInfoFast", ["GetBoardInfoFast.pyx"])]

setup(
    name='GetBoardInfoFast',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

# UndoFast
ext_modules = [Extension("UndoFast", ["UndoFast.pyx"])]

setup(
    name='UndoFast',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

# PutDiscFast
ext_modules = [Extension("PutDiscFast", ["PutDiscFast.pyx"])]

setup(
    name='PutDiscFast',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

# CyBoard8_64bit
ext_modules = [Extension("CyBoard8_64bit", ["CyBoard8_64bit.pyx"])]

setup(
    name='CyBoard8_64bit',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

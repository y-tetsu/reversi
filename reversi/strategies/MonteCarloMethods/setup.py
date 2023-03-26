from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


# PlayoutSize8_64bit
ext_modules = [Extension("PlayoutSize8_64bit", ["PlayoutSize8_64bit.pyx"])]

setup(
    name='PlayoutSize8_64bit',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

# NextMoveSize8_64bit
ext_modules = [Extension("NextMoveSize8_64bit", ["NextMoveSize8_64bit.pyx", "xorshift.c"])]

setup(
    name='NextMoveSize8_64bit',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

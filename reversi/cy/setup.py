from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# Cythonized Methods
module_names = [
    'ReversiMethods',
]

ext_modules = []
for name in module_names:
    ext_modules.append(Extension(name, [name + '.pyx']))

setup(
    name='cython_reversi_methods',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

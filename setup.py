from setuptools import setup
from distutils.extension import Extension
from reversi import __version__

setup(
    name='reversi',
    version=__version__,
    license='MIT License',
    install_requires=['cython', 'numpy', 'pyinstaller'],
    description='A reversi library for Python',
    author='y-tetsu',
    url='',
    packages=['reversi', 'reversi.BitBoardMethods', 'reversi.strategies', 'reversi.strategies.common', 'reversi.strategies.coordinator', 'reversi.genetic_algorithm'],
    ext_modules=[Extension('reversi.BitBoardMethods', ['GetBoardInfoFast.cp37-win_amd64.pyd', 'GetLegalMovesFast.cp37-win_amd64.pyd'])],
)

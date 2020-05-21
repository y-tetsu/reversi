from setuptools import setup
from distutils.extension import Extension

setup(
    name='reversi',
    version='0.0.13',
    license='MIT License',
    install_requires=['cython', 'numpy', 'pyinstaller'],
    description='A reversi library for Python',
    author='y-tetsu',
    url='',
    packages=['reversi', 'reversi.BitBoardMethods', 'reversi.strategies', 'reversi.strategies.common', 'reversi.strategies.coordinator', 'reversi.genetic_algorithm'],
    ext_modules=[
        Extension('reversi.BitBoardMethods.GetBoardInfoFast', ['reversi/BitBoardMethods/GetBoardInfoFast.c']),
        Extension('reversi.BitBoardMethods.GetLegalMovesFast', ['reversi/BitBoardMethods/GetLegalMovesFast.c']),
    ],
)

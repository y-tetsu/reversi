from setuptools import setup
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
    data_files=[('reversi.BitBoardMethods', ['GetBoardInfoFast.pyx', 'GetLegalMovesFast.pyx'])],
)

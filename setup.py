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
    packages=['reversi'],
)

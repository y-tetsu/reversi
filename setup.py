from setuptools import setup
from distutils.extension import Extension

setup(
    name='reversi',
    version='0.0.13',
    license='MIT License',
    install_requires=[
        'cython',
        'numpy',
        'pyinstaller',
    ],
    description='A reversi library for Python',
    author='y-tetsu',
    url='',
    packages=[
        'reversi',
        'reversi.BitBoardMethods',
        'reversi.strategies',
        'reversi.strategies.common',
        'reversi.strategies.coordinator',
        'reversi.genetic_algorithm',
        'reversi.examples',
        'reversi.examples.extra',
        'reversi.examples.extra.perl.bottomright',
        'reversi.examples.extra.python.topleft',
        'reversi.examples.extra.vbscript.randomcorner',
        'reversi.examples.extra.sample_input',
    ],
    package_data={
        "": ["*.json", "*.pl", "*.py", "*.vbs", "*.txt", "*.pyx", "*.pyd"]
    },
    entry_points={
        "console_scripts": [
            "install_reversi_examples=reversi.examples:install",
        ]
    },
)

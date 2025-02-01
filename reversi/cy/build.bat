::build *.pyd
py -3.7 setup.py build_ext --inplace
py -3.8 setup.py build_ext --inplace
py -3.9 setup.py build_ext --inplace

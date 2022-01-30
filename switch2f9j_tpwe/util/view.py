#!/usr/bin/env python
"""
json表示
"""
import os
import sys
import json
import pprint


if __name__ == '__main__':
    json_file = sys.argv[1]

    if os.path.isfile(json_file):
        with open(json_file) as f:
            population = json.load(f)
            pprint.pprint(population)

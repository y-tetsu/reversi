#!/usr/bin/env python
"""
経緯のチェック
"""
import os
import json


if __name__ == '__main__':
    #print('generation\tfitness\tcorner\tc\ta1\ta2\tb\to\tx\twp\twe')
    print('generation\tfitness\tcorner\tc\ta1\ta2\tb\to\tx')

    i = 0
    while True:
        json_file = './population' + str(i) + '.json'
        if os.path.isfile(json_file):
            with open(json_file) as f:
                population = json.load(f)
                fitnesses = population['fitness']
                fitness = max(fitnesses)
                max_index = fitnesses.index(fitness)

                corner = population['corner'][max_index]
                c = population['c'][max_index]
                a1 = population['a1'][max_index]
                a2 = population['a2'][max_index]
                b = population['b'][max_index]
                o = population['o'][max_index]
                x = population['x'][max_index]
                #wp = population['wp'][max_index]
                #we = population['we'][max_index]

            #text = "\t".join([str(param) for param in [i, format(fitness, '.1f'), corner, c, a1, a2, b, o, x, wp, we]])
            text = "\t".join([str(param) for param in [i, format(fitness, '.1f'), corner, c, a1, a2, b, o, x]])

            print(text)
        else:
            break
        i += 1

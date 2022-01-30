"""Select next populations by roulette
"""

import json
from random import randint, choices


POPULATIONS_CLASSES = 6
POPULATIONS_NUM = 12
GENERATION = 1200


if __name__ == '__main__':
    next_populations = {
        'generation': GENERATION,
        'corner': [],
        'c': [],
        'a1': [],
        'a2': [],
        'b1': [],
        'b2': [],
        'b3': [],
        'x': [],
        'o1': [],
        'o2': [],
        'wp': [],
        'ww': [],
        'we': [],
        'fitness': [],
    }

    for _ in range(POPULATIONS_NUM):
        cls_num = randint(1, POPULATIONS_CLASSES)
        print('    num', cls_num)

        # load json
        with open('./6th/populations' + str(cls_num) + '/population.json') as f:
            setting = json.load(f)

        # select population by roulette
        fitness = setting['fitness']
        print('        ', fitness)
        individual_num = choices(range(POPULATIONS_NUM), weights=fitness, k=1)[0]
        print('            individual_num', individual_num)

        # add new populations
        next_populations['corner'].append(setting['corner'][individual_num])
        next_populations['c'].append(setting['c'][individual_num])
        next_populations['a1'].append(setting['a1'][individual_num])
        next_populations['a2'].append(setting['a2'][individual_num])
        next_populations['b1'].append(setting['b1'][individual_num])
        next_populations['b2'].append(setting['b2'][individual_num])
        next_populations['b3'].append(setting['b3'][individual_num])
        next_populations['x'].append(setting['x'][individual_num])
        next_populations['o1'].append(setting['o1'][individual_num])
        next_populations['o2'].append(setting['o2'][individual_num])
        next_populations['wp'].append(setting['wp'][individual_num])
        next_populations['ww'].append(setting['ww'][individual_num])
        next_populations['we'].append(setting['we'][individual_num])
        next_populations['fitness'].append(setting['fitness'][individual_num])

    print()
    print('    fitness', next_populations['fitness'])

    with open('./population.json', 'w') as f:
        json.dump(next_populations, f)

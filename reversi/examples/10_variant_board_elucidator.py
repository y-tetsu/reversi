"""A example of variant-board elucidator
"""

import os
import re
import json

from reversi import BitBoard, Elucidator
from reversi import C as c


DO_RANDOM_MOVE_MATCHES = True
DO_BEST = True
DO_MAX = True
DO_SHORTEST = True
VERIFY_RECORD = True

RANDOM_MATCH = 10000
CONTROLL = {
    # name         : [random, best,  max,   shortest]
    'X'            : [False,  False, False, False],  # noqa: E203
    'x'            : [False,  False, False, False],  # noqa: E203
    'Cross'        : [False,  False, False, False],  # noqa: E203
    'Plus'         : [False,  False, False, False],  # noqa: E203
    'Drone-8'      : [False,  False, False, False],  # noqa: E203
    'Drone-6'      : [False,  False, False, False],  # noqa: E203
    'Kazaguruma-8' : [False,  False, False, False],  # noqa: E203
    'Kazaguruma-6' : [False,  False, False, False],  # noqa: E203
    'Manji-8'      : [False,  False, False, False],  # noqa: E203
    'Manji-6'      : [False,  False, False, False],  # noqa: E203
    'S'            : [False,  False, False, False],  # noqa: E203
    'Random'       : [False,  False, False, False],  # noqa: E203
    'Square-8'     : [False,  False, False, False],  # noqa: E203
    'Square-6'     : [False,  False, False, False],  # noqa: E203
    'Square-4'     : [True,   True,  True,  True],   # noqa: E203
    'Rectangle'    : [False,  False, False, False],  # noqa: E203
    'Octagon'      : [False,  False, False, False],  # noqa: E203
    'Diamond'      : [False,  False, False, False],  # noqa: E203
    'T'            : [False,  False, False, False],  # noqa: E203
    'Torus'        : [False,  False, False, False],  # noqa: E203
    'Two'          : [False,  False, False, False],  # noqa: E203
    'Equal'        : [False,  False, False, False],  # noqa: E203
    'Xhole'        : [False,  False, False, False],  # noqa: E203
    'C'            : [False,  False, False, False],  # noqa: E203
    'Rainbow'      : [False,  False, False, False],  # noqa: E203
    'Pylamid'      : [False,  False, False, False],  # noqa: E203
    'Heart'        : [False,  False, False, False],  # noqa: E203
    'Waffle'       : [False,  False, False, False],  # noqa: E203
    'Bonsai'       : [False,  False, False, False],  # noqa: E203
    'Satellite'    : [False,  False, False, False],  # noqa: E203
    'Peach'        : [False,  False, False, False],  # noqa: E203
    'Pumpkin'      : [False,  False, False, False],  # noqa: E203
    'Scarab'       : [False,  False, False, False],  # noqa: E203
    'Globe'        : [False,  False, False, False],  # noqa: E203
    'E'            : [False,  False, False, False],  # noqa: E203
    'Ring'         : [False,  False, False, False],  # noqa: E203
    'Inside'       : [False,  False, False, False],  # noqa: E203
    'Outside'      : [False,  False, False, False],  # noqa: E203
    'Skull'        : [False,  False, False, False],  # noqa: E203
    'Hourglass'    : [False,  False, False, False],  # noqa: E203
    'Treasure'     : [False,  False, False, False],  # noqa: E203
    'Rosetta'      : [False,  False, False, False],  # noqa: E203
    'Chaos'        : [False,  False, False, False],  # noqa: E203
    'B'            : [False,  False, False, False],  # noqa: E203
    'Blackhole'    : [False,  False, False, False],  # noqa: E203
    'W'            : [False,  False, False, False],  # noqa: E203
    'Whitehole'    : [False,  False, False, False],  # noqa: E203
    'Reunion'      : [False,  False, False, False],  # noqa: E203
    'Universe'     : [False,  False, False, False],  # noqa: E203
    'Pioneer'      : [False,  False, False, False],  # noqa: E203
    'Chair'        : [False,  False, False, False],  # noqa: E203
    'Coffeecup'    : [False,  False, False, False],  # noqa: E203
    'House'        : [False,  False, False, False],  # noqa: E203
    'Alien'        : [False,  False, False, False],  # noqa: E203
    'Cyborg'       : [False,  False, False, False],  # noqa: E203
}


def get_board_conf_properties(conf):
    no = conf['no']
    continent = conf['continent']
    first = c.black if not int(conf['first'], 16) else c.white
    size = 8 if not int(conf['size'], 16) else 10
    hole = int('0x' + ''.join([i.replace('0x', '') for i in conf['hole']]), 16)
    ini_black = int('0x' + ''.join([i.replace('0x', '') for i in conf['init_black']]), 16)
    ini_white = int('0x' + ''.join([i.replace('0x', '') for i in conf['init_white']]), 16)
    return no, continent, first, size, hole, ini_black, ini_white


def output_file(board_conf, ex='json'):
    outfile = 'board_conf.' + ex
    deco = str
    if ex == 'json':
        outfile = 'board_conf.' + ex
        deco = decostr
    with open(outfile, "w", encoding='utf8', newline="\n") as f:
        if ex == 'json':
            f.write('{\n')
        else:
            f.write('export const boardConf = {\n')

        last = len(board_conf.keys())
        cnt = 0
        for name in board_conf.keys():
            f.write('    "' + name + '": {\n')

            # propaty
            conf = board_conf[name]
            f.write('        "no"                       : '  + str(conf['no'])                                  + ',\n')   # noqa: E221
            f.write('        "continent"                : "' + conf['continent']                                + '",\n')  # noqa: E221
            f.write('        "type"                     : "' + conf['type']                                     + '",\n')  # noqa: E221
            f.write('        "negative"                 : '  + deco(conf['negative'])                           + ',\n')   # noqa: E221
            f.write('        "first"                    : '  + deco(conf['first'])                              + ',\n')   # noqa: E221
            f.write('        "size"                     : '  + deco(conf['size'])                               + ',\n')   # noqa: E221
            f.write('        "hole"                     : [' + ", ".join([deco(h) for h in conf['hole']])       + '],\n')  # noqa: E221
            f.write('        "color_code"               : "' + conf['color_code']                               + '",\n')  # noqa: E221
            f.write('        "init_black"               : [' + ", ".join([deco(h) for h in conf['init_black']]) + '],\n')  # noqa: E221
            f.write('        "init_white"               : [' + ", ".join([deco(h) for h in conf['init_white']]) + '],\n')  # noqa: E221
            f.write('        "init_green"               : [' + ", ".join([deco(h) for h in conf['init_green']]) + '],\n')  # noqa: E221
            f.write('        "init_ash"                 : [' + ", ".join([deco(h) for h in conf['init_ash']])   + '],\n')  # noqa: E221
            f.write('        "black"                    : '  + '[]'                                             + ',\n')   # noqa: E221
            f.write('        "white"                    : '  + '[]'                                             + ',\n')   # noqa: E221
            f.write('        "squares"                  : "' + conf['squares']                                  + '",\n')  # noqa: E221
            f.write('        "blanks"                   : '  + str(conf['blanks'])                              + ',\n')   # noqa: E221
            f.write('        "random_10000_matches"     : "' + conf['random_10000_matches']                     + '",\n')  # noqa: E221
            f.write('        "best_match_winner"        : "' + conf['best_match_winner']                        + '",\n')  # noqa: E221
            f.write('        "best_match_score"         : "' + conf['best_match_score']                         + '",\n')  # noqa: E221
            f.write('        "best_match_record"        : "' + conf['best_match_record']                        + '",\n')  # noqa: E221
            f.write('        "black_max_score"          : "' + conf['black_max_score']                          + '",\n')  # noqa: E221
            f.write('        "black_max_record"         : "' + conf['black_max_record']                         + '",\n')  # noqa: E221
            f.write('        "white_max_score"          : "' + conf['white_max_score']                          + '",\n')  # noqa: E221
            f.write('        "white_max_record"         : "' + conf['white_max_record']                         + '",\n')  # noqa: E221
            f.write('        "black_shortest_move_count": '  + str(conf['black_shortest_move_count'])           + ',\n')   # noqa: E221
            f.write('        "black_shortest_record"    : "' + conf['black_shortest_record']                    + '",\n')  # noqa: E221
            f.write('        "white_shortest_move_count": '  + str(conf['white_shortest_move_count'])           + ',\n')   # noqa: E221
            f.write('        "white_shortest_record"    : "' + conf['white_shortest_record']                    + '",\n')  # noqa: E221
            f.write('        "note"                     : "' + conf['note']                                     + '"\n')   # noqa: E221

            if cnt == last - 1:
                f.write('    }\n')
            else:
                f.write('    },\n')
            cnt += 1
        f.write('}\n')


def decostr(string):
    return '"' + str(string) + '"'


def get_scores(socre):
    match = re.search(r'\(black\) (\d+) -', score)
    black_score = match.group(1)
    match = re.search(r'- (\d+) \(white\)', score)
    white_score = match.group(1)
    return int(black_score), int(white_score)


if __name__ == '__main__':
    # board conf
    board_conf_json = 'board_conf.json'
    board_conf = {}
    if os.path.isfile(board_conf_json):
        with open(board_conf_json) as f:
            board_conf = json.load(f)

    # elucidate
    for name in board_conf.keys():
        conf = board_conf[name]
        no, continent, first, size, hole, ini_black, ini_white = get_board_conf_properties(conf)

        print('-------------------------------')
        board = BitBoard(size=size, hole=hole, ini_black=ini_black, ini_white=ini_white)
        print(board)
        print('No.           :', no)
        print('cotinent      :', continent)
        print('name          :', name)
        print('size          :', size)

        conf['squares'] = "?"
        conf['blanks'] = '"?"'

        if 'random_10000_matches' not in conf:
            conf['random_10000_matches'] = "?"

        if 'best_match_winner' not in conf:
            conf['best_match_winner'] = "?"
        if 'best_match_score' not in conf:
            conf['best_match_score'] = "?"
        if 'best_match_record' not in conf:
            conf['best_match_record'] = "?"

        if 'black_max_record' not in conf:
            conf['black_max_record'] = "?"
        if 'black_max_score' not in conf:
            conf['black_max_score'] = "?"
        if 'white_max_record' not in conf:
            conf['white_max_record'] = "?"
        if 'white_max_score' not in conf:
            conf['white_max_score'] = "?"

        if 'black_shortest_move_count' not in conf or conf['black_shortest_move_count'] == '?':
            conf['black_shortest_move_count'] = '"?"'
        if 'black_shortest_record' not in conf:
            conf['black_shortest_record'] = "?"
        if 'white_shortest_move_count' not in conf or conf['white_shortest_move_count'] == '?':
            conf['white_shortest_move_count'] = '"?"'
        if 'white_shortest_record' not in conf:
            conf['white_shortest_record'] = "?"

        if name == 'Random':
            print('skip Random')
            continue
        if name == 'Chaos':
            print('skip Chaos')
            continue
        if name == 'Pioneer':
            print('skip Pioneer')
            continue

        elucidator = Elucidator(name, size, first, hole, ini_black, ini_white)

        squares = elucidator.squares
        blanks = elucidator.blanks
        conf['squares'] = squares
        conf['blanks'] = blanks
        print('squares       :', squares)
        print('blanks        :', blanks)

        if CONTROLL[name][0] and DO_RANDOM_MOVE_MATCHES:
            conf['random_10000_matches'] = elucidator.get_random_match_result(RANDOM_MATCH)

        if CONTROLL[name][1] and DO_BEST:
            conf["best_match_winner"], conf["best_match_score"], conf["best_match_record"] = elucidator.get_best_match_winner()

        if CONTROLL[name][2] and DO_MAX:
            conf["black_max_score"], conf["black_max_record"], conf["white_max_score"], conf["white_max_record"] = elucidator.get_max_winner()

        if CONTROLL[name][3] and DO_SHORTEST:
            conf["black_shortest_move_count"], conf["black_shortest_record"], conf["white_shortest_move_count"], conf["white_shortest_record"] = elucidator.get_shortest_winner()  # noqa: E501

        if VERIFY_RECORD:
            if conf["best_match_record"] != "?":
                score = conf["best_match_score"]
                black_score, white_score = get_scores(score)
                print('\n>>> verify best_match_record :', conf["best_match_record"])
                elucidator.verify_record(conf["best_match_record"], black_score=black_score, white_score=white_score)
            if conf["black_max_record"] != "?":
                score = conf["black_max_score"]
                black_score, white_score = get_scores(score)
                print('\n>>> verify black_max_record :', conf["black_max_record"])
                elucidator.verify_record(conf["black_max_record"], black_score=black_score, white_score=white_score)
            if conf["white_max_record"] != "?":
                score = conf["white_max_score"]
                black_score, white_score = get_scores(score)
                print('\n>>> verify white_max_record :', conf["white_max_record"])
                elucidator.verify_record(conf["white_max_record"], black_score=black_score, white_score=white_score)
            if conf["black_shortest_record"] != "?":
                move_count = conf["black_shortest_move_count"]
                print('\n>>> verify black_shortest_record :', conf["black_shortest_record"])
                elucidator.verify_record(conf["black_shortest_record"], move_count=move_count)
            if conf["white_shortest_record"] != "?":
                move_count = conf["white_shortest_move_count"]
                print('\n>>> verify white_shortest_record :', conf["white_shortest_record"])
                elucidator.verify_record(conf["white_shortest_record"], move_count=move_count)

    print('-------------------------------')

    # save conf
    output_file(board_conf, 'json')
    output_file(board_conf, 'js')

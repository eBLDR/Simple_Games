#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Simple SuDoKu version, by BLDR 2018
import argparse

from main.game import Game

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SuDoKu by BLDR.')
    parser.add_argument('--solve', help='Solve the SuDoKu in sudoku_data.csv', action='store_true')
    parser.add_argument('--generate', help='Generate a new SuDoKu', action='store_true')
    args = parser.parse_args()

    if not args.generate and not args.solve:
        print('See --help.')

    game = Game(generate=args.generate, solve=args.solve)
    game.run()

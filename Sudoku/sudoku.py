#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Simple Sudoku version, by BLDR 2018
import argparse

from main.game import Game

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SuDoKu by BLDR.')
    parser.add_argument('--solve', help='Solve the sudoku in sudoku_data.csv', action='store_true')
    args = parser.parse_args()

    game = Game(solve=args.solve)

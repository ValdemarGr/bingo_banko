import sys
import argparse
from argparse import ArgumentParser, Namespace
# from typing import List, Dict, Any, Callable, Tuple
# import msvcrt
import random
import os


def showhelp():
    print('Help:\n'
          'h: Prints help\n'
          'q: Exit\n'
          's: Show the remaining balls\n'
          'n: Next ball\n'
          'r: Go back one ball step\n'
          'c: Choose your own ball')


def main():
    parser = argparse.ArgumentParser(description='Bingo game.')  # type: ArgumentParser

    parser.add_argument('--ballcount', metavar='N', type=int,
                        help='The amount of balls in the game (ball range)', required=True)
    parser.add_argument('--recover', action='store_true',
                        help='Recovery destination (if any)')
    parsed = parser.parse_args()  # type: Namespace

    if parsed.ballcount is None:
        parser.print_help()
        exit()

    pullLst = []  # type: List[int]
    removedLst = []  # type: List[int]
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    if parsed.recover:
        fp = None
        try:
            fp = open(os.path.join(__location__, 'recovery.txt'), mode='r')
        except IOError:
            fp = open(os.path.join(__location__, 'recovery.txt'), 'a+')

        lines = [line.rstrip('\n') for line in fp]  # type: List[str]

        for e in lines:
            if e.startswith('p'):
                pullLst.append(int(e[1:]))
            else:
                removedLst.append(int(e[1:]))

        fp.close()
    else:
        pullLst = list(range(0, parsed.ballcount))
        random.shuffle(pullLst)

    showhelp()
    while len(pullLst) is not 0:
        vin = str(input())  # type: str

        if 'h' in vin:
            showhelp()
        if 's' in vin:
            print(str(sorted(pullLst)))
        if 'c' in vin:
            try:
                print('input a number from the list ' + str(sorted(pullLst)))
                num = int(input())
                if num in pullLst:
                    pullLst = list(filter(lambda x: x != num, pullLst))
                    removedLst.append(num)
                    print('chosen element was ' + str(num))
                else:
                    print(str(num) + ' not in ' + str(sorted(pullLst)))
            except Exception as e:
                print('Failed with error ' + str(e))
        if 'q' in vin:
            exit()
        if 'n' in vin:
            e = pullLst[-1]
            pullLst = pullLst[:-1]
            removedLst.append(e)
            print('Chosen element: ' +
                  str(e) +
                  '\n')
        if 'r' in vin:
            if len(removedLst) == 0:
                print("List is empty\n")
            else:
                recover = removedLst[-1]
                removedLst = removedLst[:-1]
                pullLst.append(recover)
                print('Rolled back ball ' + str(recover) + '\n')

        # save to recovery file
        fp = open(os.path.join(__location__, 'recovery.txt'), mode='w+')
        for e in pullLst:
            fp.write('p'+str(e)+'\n')

        for e in removedLst:
            fp.write('r'+str(e)+'\n')

        fp.close()
    print('no more balls')
main()

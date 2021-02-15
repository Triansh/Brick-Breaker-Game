import colorama
import os

from game import Game

if __name__ == '__main__':
    colorama.init()
    os.system('clear')
    Game().start()

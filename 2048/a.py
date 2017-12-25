#-*- coding:utf-8 -*-

import curses
from random import randrange,choice
from collections import defaultdict

#user input
letter_codes=[ord(ch) for ch in 'WASDRQwasdrq']
#user actions
actions=['Up','Left','Down','Right','Restart','Exit']
#input actions 
actions_dict=dict(zip(letter_codes,actions*2))

def get_user_action(keyboard):
    char="N"
    while char not in actions_dict:
        char=keyboard.getch()
    return actions_dict[char]
def transpose(field):


def main(stdscr):
    def init():
        #
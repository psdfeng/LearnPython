#-*- coding:utf-8 -*-

import curses
from random import randrange, choice  # generate and place new tile
from collections import defaultdict

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']  #所有的有效输入都可以转换为"上，下，左，右，游戏重置，退出"这六种行为
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']  #有效输入键是最常见的 W（上），A（左），S（下），D（右），R（重置），Q（退出），这里要考虑到大写键开启的情况，获得有效键值列表：
actions_dict = dict(zip(letter_codes, actions * 2))  #将输入与行为进行关联


def get_user_action(keyboard):  
    #阻塞+循环直到获得用户有效输入才返回对应行为：  
    char = "N"
    while char not in actions_dict:    
        char = keyboard.getch()
    return actions_dict[char]

def transpose(field):
    #矩阵转置
    return [list(row) for row in zip(*field)]

def invert(field):
    #矩阵逆转（不是逆矩阵）
    return [row[::-1] for row in field]

class GameField(object):
    #创建初始化盘的参数
    def __init__(self, height=4, width=4, win=2048):
        self.height = height          #高
        self.width = width            #宽
        self.win_value = win          #过关分数
        self.score = 0                #当前分数
        self.highscore = 0            #最高分
        self.reset()

    def reset(self):
        #重置棋盘
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move(self, direction):
        #通过对矩阵进行转置与逆转，可以直接从左移得到其余三个方向的移动操作
        def move_row_left(row):
            #一行向左合并
            def tighten(row): # 把零散的非零单元挤到一块
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                #对相邻元素进行合并
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            #先挤到一块在合并再挤到一块
            return tighten(merge(tighten(row)))

        #通过对矩阵进行转置与逆转，可以直接从左移得到其余三个方向的移动操作
        moves = {}
        moves['Left']  = lambda field:                              \
                [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves['Up']    = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves['Down']  = lambda field:                              \
                transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        #判断赢
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        #判断输
        return not any(self.move_is_possible(move) for move in actions)

    def draw(self, screen):
        #绘制游戏界面
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_separator():
            #绘制水平线
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    def spawn(self):
        #随机生成一个2或者4
        new_element = 4 if randrange(100) > 89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def move_is_possible(self, direction):
        #判断能否移动
        def row_is_left_movable(row): 
            def change(i): # true if there'll be change in i-th tile
                if row[i] == 0 and row[i + 1] != 0: # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]: # Merge
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left']  = lambda field:                              \
                any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field:                              \
                 check['Left'](invert(field))

        check['Up']    = lambda field:                              \
                check['Left'](transpose(field))

        check['Down']  = lambda field:                              \
                check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False


def main():
    print("halou")
    
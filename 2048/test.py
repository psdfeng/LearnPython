#-*- coding:utf-8 -*-


field=[[0,2,0,2],[0,0,0,0],[0,0,0,0],[1,1,0,0]]


def transpose(field):
    #矩阵转置
    return [list(row) for row in zip(*field)]


def invert(field):
    #矩阵逆转（不是逆矩阵）
    return [row[::-1] for row in field]


def main():
    print("hello")
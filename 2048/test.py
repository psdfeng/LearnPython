#-*- coding:utf-8 -*-


field=[[8,2,0,2],[0,2,2,0],[0,4,0,2],[4,4,0,0]]


def transpose(field):
    #矩阵转置
    return [list(row) for row in zip(*field)]


def invert(field):
    #矩阵逆转（不是逆矩阵）
    return [row[::-1] for row in field]


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
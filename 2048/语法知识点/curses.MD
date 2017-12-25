python curses使用
python 中curses封装了c语言的curses，把c中复杂部分简单化，比如addstr(),mvaddstr(),mvwaddstr()合并成了一个addstr()方法。

一、语法入门
1、打开和关闭一个curses 应用程序
在任何代码执行前都先要初始化curses。初始化操作就是调用initscr()函数，如下。该函数根据不同设备返回一个window对象代表整个屏幕，这个window对象通常叫做stdscr，和c语言报错一致。

import curses
stdscr = curses.initscr()
使用curses通常要关闭屏幕回显，目的是读取字符仅在适当的环境下输出。这就需要调用noecho()方法

curses.noecho()
应用程序一般是立即响应的，即不需要按回车就立即回应的，这种模式叫cbreak模式，相反的常用的模式是缓冲输入模式。开启立即cbreak模式代码如下。

curses.cbreak()
终端经常返回特殊键作为一个多字节的转义序列，比如光标键，或者导航键比如Page UP和Home键 。curses可以针对这些序列做一次处理，比如curses.KEY_LEFT返回一个特殊的值。要完成这些工作，必须开启键盘模式。

stdscr.keypad(1)
关闭curses非常简单，如下：

curses.nocbreak()#关闭字符终端功能（只有回车时才发生终端）
stdscr.keypad(0)
curses.echo() #打开输入回显功能
调用endwin()恢复默认设置

curses.endwin()
调试curses时常见的问题就是curses应用程序结束后没有重置终端到之前的状态，把终端弄的一团糟。python中该问题经常是因为代码有bug，发送异常引起的。比如键盘敲入字符后屏幕不回显，这让shell用起来非常困难。

为了避免这样的问题，可以导入curses.wrapper模块。这个函数做了一些初始化的工作，包括上面提到的和颜色的初始化。然后再执行你提供的函数，最后重置。而且被调用的函数写在try-catch中。

2、打开新窗口和pad
 通常调用initscr()获取一个window对象代表全部屏幕。但是很多程序希望划分屏幕为几个小的窗口，为了重绘，擦出这些工作在小窗口中独立进行。newwin()函数就是用来新建一个新的窗口，需要给定窗口尺寸，并返回新的window对象的。

begin_x = 20; begin_y = 7
height = 5; width = 40
win = curses.newwin(height, width, begin_y, begin_x)
注意：坐标通过是先y后x。这和别的坐标系统不同，但是根深蒂固，写的时候就这样现在改太晚喽。

当调用一个方法去显示或者擦除文本时，效果不会立即显示。 为了减少屏幕重绘的时间，curses就先累积这些操作，用一种更有效的方式去显示。就比如说你的程序先在窗口显示了几个字符，然后就清除屏幕，那就没必要发送初始字符了，因为它们不会被显示。

因此，curses需要你使用refresh()函数明确指出重绘窗口。

pad
pad是window的特例。pad可以比显示的屏幕大，一次只显示pad的一部分。创建一个pad很简单，只需要提供宽高即可。但是刷新pad需要提供屏幕上显示的部分pad的坐标。

复制代码
pad = curses.newpad(100, 100)
#  These loops fill the pad with letters; this is
# explained in the next section
for y in range(0, 100):
    for x in range(0, 100):
        try:
            pad.addch(y,x, ord('a') + (x*x+y*y) % 26)
        except curses.error:
            pass

#  Displays a section of the pad in the middle of the screen
pad.refresh(0,0, 5,5, 20,75)
复制代码
同时由多个window或者多个pad，有一问题：刷新某个window或pad时屏幕会闪烁。

避免闪烁的方法：在每个window调用noutrefresh()方法。 然后使用refresh()方法的最后再调用doupdate()方法。

3、显示文本
addscr不同格式如下：如果没有坐标，字符显示在上一次操作完的位置。

Form	Description
str or ch	Display the string str or character ch at the current position
str or ch, attr	Display the string str or character ch, using attribute attr at the current position
y, x, str or ch	Move to position y,x within the window, and display str or ch
y, x, str or ch, attr	Move to position y,x within the window, and display str or ch, using attribute attr
属性可以让文本高亮显示，比如黑体，下划线，倒序，彩色显示。

4、属性和颜色
属性和描述：

Attribute	Description
A_BLINK	Blinking text
A_BOLD	Extra bright or bold text
A_DIM	Half bright text
A_REVERSE	Reverse-video text
A_STANDOUT	The best highlighting mode available
A_UNDERLINE	Underlined text
屏幕第一行reverse-video显示。

stdscr.addstr(0, 0, "Current mode: Typing mode",
              curses.A_REVERSE)
stdscr.refresh()
curses使用前景色和背景色，可通过color_pair()方法获取一对颜色。

使用颜色对1显示一行

stdscr.addstr("Pretty text", curses.color_pair(1))
stdscr.refresh()
start_color()初始化了8中基本颜色：0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white。

init_pair(n,f,b)修改颜色对n，让f为前景色，b为背景色。颜色对0天生的黑白色，不允许改。

比如：修改color1为红色文本，白色背景：

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
使用：

stdscr.addstr(0,0, "RED ALERT!", curses.color_pair(1))
5、用户输入
获取输入一遍使用getch()方法，这个方法暂停等待用户输入，显示用echo()方法。

getch()返回一个整数 ，在0到255之间，表示输入字符的ASCII值。打印255的是些特殊字符，比如Page Up,Home。

代码经常这样写

复制代码
while 1:
    c = stdscr.getch()
    if c == ord('p'):
        PrintDocument()
    elif c == ord('q'):
        break  # Exit the while()
    elif c == curses.KEY_HOME:
        x = y = 0
复制代码
 getstr()获取一个字符串。因为功能有限不常用。

curses.echo()            # Enable echoing of characters
# Get a 15-character string, with the cursor on the top line
s = stdscr.getstr(0,0, 15)
二、例子
代码如下：

复制代码
#-*- coding: UTF-8 -*-
import curses

stdscr = curses.initscr()

def display_info(str, x, y, colorpair=2):
    '''''使用指定的colorpair显示文字'''  
    global stdscr
    stdscr.addstr(y, x,str, curses.color_pair(colorpair))
    stdscr.refresh()

def get_ch_and_continue():
    '''''演示press any key to continue'''
    global stdscr
    #设置nodelay，为0时会变成阻塞式等待
    stdscr.nodelay(0)
    #输入一个字符
    ch=stdscr.getch()
    #重置nodelay,使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)
    return True

def set_win():
    '''''控制台设置'''
    global stdscr
    #使用颜色首先需要调用这个方法
    curses.start_color()
    #文字和背景色设置，设置了两个color pair，分别为1和2
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #关闭屏幕回显
    curses.noecho()
    #输入时不需要回车确认
    curses.cbreak()
    #设置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)

def unset_win():
    '''控制台重置'''
    global stdstr
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #结束窗口
    curses.endwin()

if __name__=='__main__':
    try:
        set_win()
        display_info('Hola, curses!',0,5)
        display_info('Press any key to continue...',0,10)
        get_ch_and_continue()
    except Exception,e:
        raise e
    finally:
        unset_win()
复制代码
执行：# python testcurses.py



三、排错
报错：

复制代码
[root@yl-web-test srv]# python curses.py
Traceback (most recent call last):
  File "curses.py", line 2, in <module>
    import curses
  File "/srv/curses.py", line 4, in <module>
    stdscr = curses.initscr()
AttributeError: 'module' object has no attribute 'initscr'
复制代码
原因：因为我的文件取名是curses.py，而系统也是用的curses.py，python执行时先从当前目录查找，所以不能和系统文件重名。

换个名字，比如改名为testcurses.py 就好了。
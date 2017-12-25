import curses 

def main(stdscr):
    print("hello")
    curses.use_default_colors()

curses.wrapper(main)

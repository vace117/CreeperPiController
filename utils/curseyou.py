import curses

def init_curses():
	global stdscr
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)
	return stdscr

def restore_terminal():
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()	

def println(sstr):
	_print(str(sstr) + "\n")

def _print(sstr):
	stdscr.addstr(sstr)
	stdscr.refresh()

def print_at(y,x,sstr):
	stdscr.addstr(y,x,sstr)
	stdscr.refresh()

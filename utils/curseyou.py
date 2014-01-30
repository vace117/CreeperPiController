#!/usr/bin/python

import curses
 
def println(str):
	_print(str + "\n")

def _print(str):
	stdscr.addstr(str)
	stdscr.refresh()

def print_at(y,x,str):
	stdscr.addstr(y,x,str)
	stdscr.refresh()

try:
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)

	println("Test1")
	println("Test2")

	while True:
		key = stdscr.getch()
		if key == curses.KEY_UP:
			print_at(10, 0, "Pressed: %s" % key)
		elif key == curses.KEY_DOWN:
			print_at(10, 0, "Pressed: %s" % key)

finally:
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()	


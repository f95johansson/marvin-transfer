import curses
import os
from math import floor, ceil

from marvin.ui_column import UIColumn

def run(func):
    os.environ.setdefault('ESCDELAY', '25') # default 1000ms
    curses.wrapper(func)

def blank(*args):
    pass

class IllegalArgumentError(ValueError):
    pass
class UIError(Exception):
    pass

class Events:
    RESIZE = 'resize'
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    SPACE = 'space'
    ENTER = 'enter'
    TAB = 'tab'
    LETTER = 'letter'
    BACKSPACE = 'backspace'
    ESCAPE = 'escape'

class UI:
    event = Events()

    def __init__(self, window):
        self.window = window
        curses.curs_set(0) # hide cursor
        (self.height, self.width) = self.window.getmaxyx()
        self.left_column = UIColumn(curses.newpad(self.height-3, floor((self.width-3)/2)))
        self.right_column = UIColumn(curses.newpad(self.height-3, ceil((self.width-3)/2)))
        self.clear()

        self.running = False
        self.event_listeners = {
            UI.event.RESIZE: blank,
            UI.event.UP: blank,
            UI.event.DOWN: blank,
            UI.event.LEFT: blank,
            UI.event.RIGHT: blank,
            UI.event.SPACE: blank,
            UI.event.ENTER: blank,
            UI.event.TAB: blank,
            UI.event.LETTER: blank,
            UI.event.BACKSPACE: blank,
            UI.event.ESCAPE: blank
        }
        #self.setup_basic_events()

    def start(self):
        self.running = True

        while self.running:
            if self.window.is_wintouched():
                self.window.refresh()
            self.left_column.refresh( 0,0, 2,1, self.height-2, self.left_column.width-1)
            self.right_column.refresh( 0, 0, 2,self.left_column.width+2 , self.height-2, self.left_column.width+self.right_column.width)

            event = self.window.get_wch() # blocking

            #try:
            if event == curses.KEY_RESIZE:
                self.resize()
            elif event == curses.KEY_UP:
                self.up()
            elif event == curses.KEY_DOWN:
                self.down()
            elif event == curses.KEY_LEFT:
                self.left()
            elif event == curses.KEY_RIGHT:
                self.right()
            elif event == curses.KEY_ENTER or event == 10 or event == 13 \
                    or (type(event) == str and (ord(event) == 10 or ord(event) == 13)):
                self.enter()
            elif event == curses.KEY_BACKSPACE or event == 8 or event == 127 \
                    or (type(event) == str and (ord(event) == 8 or ord(event) == 127)):
                self.backspace()
            elif event == '\t':
                self.tab()
            elif event == ' ':
                self.space()
            elif event == 27 or (type(event) == str and ord(event) == 27): # Esc or Alt
                self.window.nodelay(True)
                c = self.window.getch()
                if c == -1 or c == 27: # Esc
                    self.escape()
                else: # Alt
                    pass
                self.window.nodelay(False)


            elif type(event) == str: # Assumes letter
                self.letter(event)
            else:
                self.print_status_bar(str(event))


            #except curses.error:
            #    raise UIError('Invalid UI operation')


    def quit(self):
        self.running = False

    def clear(self, column=None):
        if column == None:
            self.window.clear()
            self.window.vline(1, self.left_column.width, '|', self.height-3)
        elif column == self.left_column:
            column.clear()
            self.left_column.refresh( 0,0, 2,1, self.height-2, self.left_column.width-1)
        elif column == self.right_column:
            column.clear()
            self.right_column.refresh( 0, 0, 2,self.left_column.width+2 , self.height-2, self.left_column.width+self.right_column.width)

    def add_string(self, x, y, string, filled=False):
        if filled:
            self.window.addstr(y, x, string, curses.A_REVERSE)
        else:
            self.window.addstr(y, x, string)

    def delete_string(self, x, y, lenght):
        for i in range(0, lenght):
            self.window.delch(y, x+i)

    def print_status_bar(self, string):
        self.clear_status_bar()
        self.window.addstr(self.height-2, 3, string[:self.width-5])
        self.window.refresh()

    def clear_status_bar(self):
        self.window.move(self.height-2, 3)
        self.window.deleteln()

    def add_eventlistener(self, event, func):
        try:
            self.event_listeners[event]
            self.event_listeners[event] = func
        except KeyError:
            raise IllegalArgumentError('No such event ({})'.format(event))

    def setup_basic_events(self):
        for event in self.event_listeners:
            try:
                getattr(self, event)
            except:
                def basic_event(self):
                    self.event_listeners[event]()

                setattr(self, event, basic_event)#lambda self: pdb.set_trace())#self.event_listeners[event]())


    # Events
    def resize(self):
        (self.height, self.width) = self.window.getmaxyx()
        self.left_column.resize(self.height-3, floor((self.width-3)/2))
        self.right_column.resize(self.height-3, ceil((self.width-3)/2))
        self.window.vline(1, self.left_column.width, '|', self.height-3)
        self.event_listeners[UI.event.RESIZE](self.width, self.height)

    def up(self):   
        self.event_listeners[UI.event.UP]()

    def down(self):
        self.event_listeners[UI.event.DOWN]()

    def left(self):
        self.event_listeners[UI.event.LEFT]()

    def right(self):
        self.event_listeners[UI.event.RIGHT]()

    def space(self):
        self.event_listeners[UI.event.SPACE]()

    def enter(self):
        self.event_listeners[UI.event.ENTER]()

    def tab(self):
        self.event_listeners[UI.event.TAB]()

    def letter(self, letter):
        self.event_listeners[UI.event.LETTER](letter)

    def backspace(self):
        self.event_listeners[UI.event.BACKSPACE]()

    def escape(self):
        self.event_listeners[UI.event.ESCAPE]()

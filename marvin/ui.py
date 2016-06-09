import curses
from math import floor, ceil

from marvin.ui_column import UIColumn

def run(func):
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
    Q = 'q'
    SPACE = ' '
    ENTER = 'enter'

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
            UI.event.Q: blank,
            UI.event.SPACE: blank,
            UI.event.ENTER: blank
        }
        #self.setup_basic_events()

    def start(self):
        self.running = True

        while self.running:
            if self.window.is_wintouched():
                self.window.refresh()
            self.left_column.refresh( 0,0, 2,1, self.height-2, self.left_column.width-1)
            self.right_column.refresh( 0, 0, 2,self.left_column.width+1 , self.height-2, self.left_column.width+self.right_column.width-1)

            event = self.window.getch() # blocking

            #try:
            if event == curses.KEY_RESIZE:
                self.resizing()
            elif event == curses.KEY_UP:
                self.up()
            elif event == curses.KEY_DOWN:
                self.down()
            elif event == curses.KEY_LEFT:
                self.left()
            elif event == curses.KEY_RIGHT:
                self.right()
            elif event == ord('q'):
                self.q()
            elif event == ord(' '):
                self.space()
            elif event == curses.KEY_ENTER or event == 10 or event == 13:
                self.enter()

            #except curses.error:
            #    raise UIError('Invalid UI operation')


    def quit(self):
        self.running = False

    def clear(self):
        self.window.clear()
        self.window.vline(1, self.left_column.width, '|', self.height-3)


    def add_string(self, x, y, string, filled=False):
        if filled:
            self.window.addstr(y, x, string, curses.A_REVERSE)
        else:
            self.window.addstr(y, x, string)

    def delete_string(self, x, y, lenght):
        for i in range(0, lenght):
            self.window.delch(y, x+i)

    def add_eventlistener(self, event, func):
        try:
            self.event_listeners[event]
            self.event_listeners[event] = func
        except KeyError:
            raise IllegalArgumentError('No such event ({})'.format(event))

    # Events
    def resizing(self):
        (self.height, self.width) = self.window.getmaxyx()
        self.left_column.resize(self.height-3, floor((self.width-3)/2))
        self.right_column.resize(self.height-3, ceil((self.width-3)/2))
        self.window.vline(1, self.left_column.width, '|', self.height-3)
        self.event_listeners[UI.event.RESIZE](self.width, self.height)

    def setup_basic_events(self):
        for event in self.event_listeners:
            try:
                getattr(self, event)
            except:
                def basic_event():
                    self.event_listeners[event]()

                setattr(self, event, basic_event)#lambda self: pdb.set_trace())#self.event_listeners[event]())


    def up(self):
        self.event_listeners[UI.event.UP]()

    def down(self):
        self.event_listeners[UI.event.DOWN]()

    def left(self):
        self.event_listeners[UI.event.LEFT]()

    def right(self):
        self.event_listeners[UI.event.RIGHT]()

    def q(self):
        self.event_listeners[UI.event.Q]()

    def space(self):
        self.event_listeners[UI.event.SPACE]()

    def enter(self):
        self.event_listeners[UI.event.ENTER]()


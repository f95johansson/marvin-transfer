# -*- coding: utf-8 -*-
"""Takes care of the ui of the application"""

import curses
import os
from math import floor
from math import ceil

from marvin.ui_column import UIColumn

def run(func):
    """Wrapper for a main run function"""
    os.environ.setdefault('ESCDELAY', '25') # default 1000ms
    curses.wrapper(func)

def blank(*args, **kwargs):
    """This function does absolutely nothing"""

class IllegalArgumentError(ValueError):
    """Error for invalid arguments"""
    
class UIError(Exception):
    """Error within the UI"""

class Events:
    """Events for with class UI will respond to"""

    def __init__(self):
        """Setup all the events"""
        self.RESIZE = 'resize'
        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'
        self.SPACE = 'space'
        self.ENTER = 'enter'
        self.TAB = 'tab'
        self.LETTER = 'letter'
        self.BACKSPACE = 'backspace'
        self.ESCAPE = 'escape'
        self.CTRL_D = 'ctrl_d'


class UI:
    """Curses ui with a two column list design

    Will fire event listeners when appropriate
    """
    event = Events()

    def __init__(self, window):
        """Setup visuel elements, such as the two colums and title bar"""
        self.window = window
        curses.use_default_colors() # take colors from terminal
        curses.curs_set(0) # hide cursor
        (self.height, self.width) = self.window.getmaxyx()
        self.left_column = UIColumn(curses.newpad(self.height-3, int(floor((self.width-3)/2))))
        self.right_column = UIColumn(curses.newpad(self.height-3, int(ceil((self.width-3)/2))))
        self.clear()

        self.left_title = ''
        self.right_title = ''

        self.running = False
        self.event_listeners = {}
        for event in vars(UI.event).values():
            self.event_listeners[event] = blank # setup empty function as default for all events

    def run(self):
        """A loop which will fire event listeners based on user input"""
        self.running = True

        while self.running:
            if self.window.is_wintouched():
                self.window.refresh()
            self.left_column.refresh( 0,0, 2,1, self.height-2, self.left_column.width-1)
            self.right_column.refresh( 0,0, 2,self.left_column.width+2 , self.height-2, self.left_column.width+self.right_column.width)

            try:
                event = self.window.get_wch() # blocking
            except AttributeError:
                event = self.get_wch_compatibility_layer()
            except curses.error:
                event = None


            #try:
            if event == -1:
                pass

            elif event == curses.KEY_RESIZE:
                self.resize()
                self.event_listeners[UI.event.RESIZE](self.width, self.height)

            elif event == curses.KEY_UP:
                self.event_listeners[UI.event.UP]()

            elif event == curses.KEY_DOWN:
                self.event_listeners[UI.event.DOWN]()

            elif event == curses.KEY_LEFT:
                self.event_listeners[UI.event.LEFT]()

            elif event == curses.KEY_RIGHT:
                self.event_listeners[UI.event.RIGHT]()

            elif event == curses.KEY_ENTER or event == '\n' or event == '\r':
                self.event_listeners[UI.event.ENTER]()

            elif event == curses.KEY_BACKSPACE or event == 8 or event == 127 \
                    or (type(event) == str and (ord(event) == 8 or ord(event) == 127)):
                self.event_listeners[UI.event.BACKSPACE]()

            elif event == '\t':
                self.event_listeners[UI.event.TAB]()

            elif event == ' ':
                self.event_listeners[UI.event.SPACE]()

            elif event == 27 or (type(event) == str and ord(event) == 27): # Esc or Alt
                self.window.nodelay(True)
                c = self.window.getch()
                if c == -1 or c == 27: # Esc
                    self.event_listeners[UI.event.ESCAPE]()
                else: # Alt
                    pass
                self.window.nodelay(False)

            elif type(event) == str: # Assumes letter
                self.event_listeners[UI.event.LETTER](event)


            #except curses.error:
            #    raise UIError('Invalid UI operation')


    def quit(self):
        """Exits the ui and the run wrapper"""
        self.running = False

    def clear(self, column=None):
        """Clears the entire window if no column is supplied, otherwise only column"""
        if column == None:
            self.window.clear()
            self.window.vline(1, self.left_column.width, '|', self.height-2)
        elif column == self.left_column:
            column.clear()
            self.left_column.refresh( 0,0, 2,1, self.height-2, self.left_column.width-1)
        elif column == self.right_column:
            column.clear()
            self.right_column.refresh( 0, 0, 2,self.left_column.width+2 , self.height-2, self.left_column.width+self.right_column.width)

    def set_title_bar(self, left_title=None, right_title=None):
        """Set the two titles above each column"""
        self.left_title = self.left_title if left_title == None else left_title
        self.right_title = self.right_title if right_title == None else right_title
        self._update_title_bar()

    def _update_title_bar(self):
        """Repaint title bar"""
        string = ' {title: <{lfill}} {rtitle: <{rfill}} ' \
            .format(title=self.left_title, lfill=str(self.left_column.width), \
                    rtitle=self.right_title, rfill=str(self.right_column.width))
        self.window.addstr(0, 0, string, curses.A_REVERSE)

    def print_status_bar(self, string):
        """Print message in status bar, will desepear on clear()"""
        self.clear_status_bar()
        self.window.addnstr(self.height-2, 3, string, self.width-4)
        self.window.refresh()

    def clear_status_bar(self):
        """Remove message in status bar"""
        self.window.move(self.height-2, 3)
        self.window.deleteln()

    def add_eventlistener(self, event, func):
        """Add event listener to an event from specified in Event class"""
        try:
            self.event_listeners[event]
            self.event_listeners[event] = func
        except KeyError:
            raise IllegalArgumentError('No such event ({})'.format(event))

    def resize(self):
        """Resize ui and repaint all objects"""
        (self.height, self.width) = self.window.getmaxyx()
        self.window.clear()
        self.left_column.resize(self.height-3, floor((self.width-3)/2))
        self.right_column.resize(self.height-3, ceil((self.width-3)/2))
        self.window.vline(1, self.left_column.width, '|', self.height-2)
        self._update_title_bar()

    def get_wch_compatibility_layer(self):
        """Support curses.get_wch() in older python versions (<3.3)"""
        ch = self.window.getch()
        if ch > 256 or ch == -1:
            return ch

        self.window.nodelay(True)

        w_ch_list = [chr(ch)]
        while True:
            ch = self.window.getch()
            if ch == -1:
                break
            elif ch > 256:
                self.window.ungetch(ch)
                break
            else:
                w_ch_list.append(chr(ch))

        self.window.nodelay(False)

        w_ch = ''.join(w_ch_list)

        return -1 if len(w_ch_list) > 1 else w_ch_list[0]





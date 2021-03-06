# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import curses
from marvin.marked_list import MarkedList

class UIColumn:

    def __init__(self, window):
        self.window = window
        (self.height, self.width) = self.window.getmaxyx()
        self.content = MarkedList()
        self.marked_positions = set()
        self.focused = False
        self.scrolled = 0
        self.ascii_message = '--Name hidden, only ascii supported--'

    def update_content(self, content):
        self.scrolled = 0
        self.content = content
        self.window.resize(len(content), self.width)
        (self.height, self.width) = self.window.getmaxyx()
        self._draw()

    def resize(self, height, width):
        self.window.resize(self.height, int(width))
        self.window.touchwin()
        self.scrolled = 0
        (_, self.width) = self.window.getmaxyx()
        self._draw()

    def scroll(self, length=1):
        self.scrolled += length

    def refresh(self, y, x, min_row, min_col, max_row, max_col):
        if self.window.is_wintouched():
            try:
                self.window.refresh(y+self.scrolled, x, min_row, 
                                    min_col, max_row, max_col)
            except curses.error:
                """This error occur when resizing terminal window in both
                width and height in a fast motion.
                I can't figure out why this error occur and the curses stupid
                c error messages isn't any help either. So for now, I leave it
                """

    def _draw(self):
        for i, value in enumerate(self.content):
            if (i >= self.height):
                break

            if i in self.marked_positions:
                if self.focused:
                    self._add_background(i)
                else:
                    self._add_underline(i)
            else:
                try:
                    if self.content.is_marked(i):
                        self._add_bold(i)
                    else:
                        self._add_string(i)
                except AttributeError:
                    self._add_string(i)


    def clear(self):
        self.window.erase()

    def mark_position(self, index):
        self.marked_positions.add(index)
        if self.focused:
            self._add_background(index)
        else:
            self._add_underline(index)

    def unmark_position(self, index):
        try:
            self.marked_positions.remove(index)
            self._remove_background(index)
        except KeyError:
            pass

    def reset_positions(self):
        self.marked_positions.clear()

    def _add_string(self, index):
        string = self.content[index][:self.width-1]
        try:
            self.window.addstr(index, 0, string)
        except UnicodeEncodeError:
            self.window.addstr(index, 0, string.encode('utf-8'))

    def _add_background(self, index):
        string = self.content[index][:self.width-1]
        try:
            self.window.addstr(index, 0, string, curses.A_REVERSE)
        except UnicodeEncodeError:
            self.window.addstr(index, 0, string.encode('utf-8'), curses.A_REVERSE)

    def _add_underline(self, index):
        string = self.content[index][:self.width-1]
        try:
            self.window.addstr(index, 0, string, curses.A_UNDERLINE)
        except UnicodeEncodeError:
            self.window.addstr(index, 0, string.encode('utf-8'), curses.A_UNDERLINE)

    def _add_bold(self, index):
        string = self.content[index][:self.width-1]
        try:
            self.window.addstr(index, 0, string, curses.A_BOLD)
        except UnicodeEncodeError:
            self.window.addstr(index, 0, string.encode('utf-8'), curses.A_BOLD)

    def _remove_background(self, index):
        try:
            if self.content.is_marked(index):
                self._add_bold(index)
            else:
                self._add_string(index)
        except AttributeError:
            self._add_string(index)


    def focus(self):
        self.focused = True
        for i in self.marked_positions:
            self._add_background(i)

    def unfocus(self):
        self.focused = False
        for i in self.marked_positions:
            self._add_underline(i)


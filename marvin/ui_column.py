import curses

class UIColumn:

    def __init__(self, window):
        self.window = window
        (self.height, self.width) = self.window.getmaxyx()
        self.content = []
        self.marked_positions = set()
        self.focused = False
        self.scrolled = 0

    def update_content(self, content):
        self.scrolled = 0
        self.content = content
        self.window.resize(len(content), self.width)
        (self.height, self.width) = self.window.getmaxyx()
        self.draw()

    def resize(self, width, height):
        self.window.resize(height, width)
        (self.height, self.width) = self.window.getmaxyx()

    def scroll(self, length=1):
        self.scrolled += length

    def refresh(self, y, x, min_col, min_row, max_col, max_row):
        if self.window.is_wintouched():
            self.window.refresh(y+self.scrolled, x, min_col, min_row, max_col, max_row)

    def draw(self):
        for i, value in enumerate(self.content):
            if (i >= self.height):
                break

            if i in self.marked_positions:
                if self.focused:
                    self.window.addstr(i, 0, value[:self.width-1], curses.A_REVERSE)
                else:
                    self.window.addstr(i, 0, value[:self.width-1], curses.A_UNDERLINE)
            else:
                self.window.addstr(i, 0, value[:self.width-1])

    def clear(self):
        string = ' '*(self.width-1)
        for i in range(self.height):
            self.window.addstr(i, 0, string)

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

    def _add_background(self, index):
        string = self.content[index][:self.width-1]
        self.window.addstr(index, 0, string, curses.A_REVERSE)

    def _add_underline(self, index):
        string = self.content[index][:self.width-1]
        self.window.addstr(index, 0, string, curses.A_BOLD)

    def _remove_background(self, index):
        string = self.content[index][:self.width-1]
        self.window.addstr(index, 0, string)

    def focus(self):
        self.focused = True
        for i in self.marked_positions:
            self._add_background(i)

    def unfocus(self):
        self.focused = False
        for i in self.marked_positions:
            self._add_underline(i)


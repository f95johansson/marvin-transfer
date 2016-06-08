import curses

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

class UI:
    event = Events()

    def __init__(self, window):
        self.window = window
        curses.curs_set(0) # hide cursor
        self.window.clear()

        self.event_listeners = {
            UI.event.RESIZE: blank,
            UI.event.UP: blank,
            UI.event.DOWN: blank,
            UI.event.LEFT: blank,
            UI.event.RIGHT: blank
        }

    def start(self):

        while True:
            self.window.refresh()
            # wait
            event = self.window.getch()

            try:
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

            except curses.error:
                raise UIError('Invalid UI operation')

    def close(self):
        pass

    def add_string(self, x, y, string):
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
        (height, width) = self.window.getmaxyx()
        self.event_listeners[UI.event.RESIZE](width, height)

    def up(self):
        self.event_listeners[UI.event.UP]()

    def down(self):
        self.event_listeners[UI.event.DOWN]()

    def left(self):
        self.event_listeners[UI.event.LEFT]()

    def right(self):
        self.event_listeners[UI.event.RIGHT]()
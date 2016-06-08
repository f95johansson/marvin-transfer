from ui import UI
import os

class App:

    def __init__(self):
        self.x = 0
        self.y = 0

        self.current_path = os.getcwd()
        self.current_files = os.listdir(self.current_path)

    def run(self, window):
        self.ui = UI(window)
        self.ui.add_eventlistener(UI.event.RESIZE, self.resize)

        self.ui.add_eventlistener(UI.event.UP, self.up)
        self.ui.add_eventlistener(UI.event.DOWN, self.down)
        self.ui.add_eventlistener(UI.event.LEFT, self.left)
        self.ui.add_eventlistener(UI.event.RIGHT, self.right)

        self.ui.add_string(0, 0, '0')
        for i, file in enumerate(self.current_files):
            self.ui.add_string(1, 1+i, file)

        self.ui.start() # blocking


    def resize(self, width, height):
        self.ui.add_string(0, 0, 'resizing')

    def up(self):
        self.ui.delete_string(self.x, self.y, 1)
        self.y -= 1
        self.ui.add_string(self.x, self.y, '0')

    def down(self):
        self.ui.delete_string(self.x, self.y, 1)
        self.y += 1
        self.ui.add_string(self.x, self.y, '0')

    def left(self):
        self.ui.delete_string(self.x, self.y, 1)
        self.x -= 1
        self.ui.add_string(self.x, self.y, '0')

    def right(self):
        self.ui.delete_string(self.x, self.y, 1)
        self.x += 1
        self.ui.add_string(self.x, self.y, '0')
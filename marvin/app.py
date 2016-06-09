from marvin.ui import UI
from marvin.file_manager import FileManager
from marvin.adb import ADB

class App:

    def __init__(self):
        self.adb = ADB()
        self.fm = FileManager()
        self.focused = self.adb
        self.focused_column = None

    def run(self, window):
        self.ui = UI(window)
        self.focused_column = self.ui.left_column

        self.ui.add_eventlistener(UI.event.RESIZE, self.resize)
        self.ui.add_eventlistener(UI.event.UP, self.up)
        self.ui.add_eventlistener(UI.event.DOWN, self.down)
        self.ui.add_eventlistener(UI.event.LEFT, self.left)
        self.ui.add_eventlistener(UI.event.RIGHT, self.right)
        self.ui.add_eventlistener(UI.event.Q, self.quit)
        self.ui.add_eventlistener(UI.event.SPACE, self.switch)

        self.update_file_list(manager=self.adb, manager_column=self.ui.left_column)
        self.update_file_list(manager=self.fm, manager_column=self.ui.right_column)

        self.ui.add_string(0, 0, self.adb.get_device_name(), filled=True)

        self.ui.start() # blocking

    def update_file_list(self, manager=None, manager_column=None):
        manager = self.focused if manager == None else manager
        manager_column = self.focused_column if manager_column == None else manager_column

        if len(manager.listdir()) > 0:
            manager_column.reset_positions()
            manager_column.update_content(manager.listdir())
            manager_column.mark_position(manager.get_position())
        else:
            manager_column.reset_positions()
            manager_column.update_content(['--Empty--'])

    def resize(self, width, height):
        self.ui.add_string(0, 0, 'resizing')

    def up(self):
        self.focused_column.unmark_position(self.focused.get_position())
        self.focused.move_up()
        self.focused_column.mark_position(self.focused.get_position())

    def down(self):
        self.focused_column.unmark_position(self.focused.get_position())
        self.focused.move_down()
        self.focused_column.mark_position(self.focused.get_position())

    def left(self):
        success = self.focused.cd_out()
        if success:
            self.update_file_list()

    def right(self):
        success = self.focused.cd_in()
        if success:
            self.update_file_list()

    def switch(self):
        if self.focused == self.adb:
            self.focused = self.fm
            self.focused_column = self.ui.right_column
        else:
            self.focused = self.adb
            self.focused_column = self.ui.left_column

    def quit(self):
        self.ui.quit()



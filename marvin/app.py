# -*- coding: utf-8 -*-
"""Contains App class which runs the whole application"""

from marvin.ui import UI
from marvin.file_manager import FileManager
from marvin.adb import ADB

class App:
    """App takes care of all the possible interaction the user have""" 

    def __init__(self):
        """Sets up the file managers for both local and android device"""
        self.adb = ADB()
        self.fm = FileManager()
        self.focused = self.fm
        self.focused_column = None

    def start(self, window):
        """Setup the ui and and the handlers for events"""
        self.ui = UI(window)
        self.focused_column = self.ui.left_column
        self.focused_column.focused = True

        self.ui.add_eventlistener(UI.event.RESIZE, self.resize)
        self.ui.add_eventlistener(UI.event.UP, self.move_up)
        self.ui.add_eventlistener(UI.event.DOWN, self.move_down)
        self.ui.add_eventlistener(UI.event.LEFT, self.cd_out)
        self.ui.add_eventlistener(UI.event.RIGHT, self.cd_in)
        self.ui.add_eventlistener(UI.event.ESCAPE, self.quit)
        self.ui.add_eventlistener(UI.event.SPACE, self.switch)
        self.ui.add_eventlistener(UI.event.TAB, self.switch)
        self.ui.add_eventlistener(UI.event.ENTER, self.transfer)
        self.ui.add_eventlistener(UI.event.LETTER, self.letter_input)
        self.ui.add_eventlistener(UI.event.BACKSPACE, self.backspace)

        self.update_file_list(manager=self.adb, manager_column=self.ui.right_column)
        self.update_file_list(manager=self.fm, manager_column=self.ui.left_column)

        self.ui.set_title_bar('Local', self.adb.get_device_name())

        self.ui.run() # blocking

    def update_file_list(self, manager=None, manager_column=None, empty_message='--Empty--'):
        """Update list of file and folders
        If parameters manager and manager_column is not given, their assumed
        to be the focused ones
        """
        manager = self.focused if manager == None else manager
        manager_column = self.focused_column if manager_column == None else manager_column

        self.ui.clear(manager_column) # must clear & refresh window before resizing pad 
                                      # (done in update_content())

        if len(manager.listdir()) > 0:
            manager_column.reset_positions()
            manager_column.update_content(manager.listdir())
            manager_column.mark_position(manager.get_position())
        else:
            manager_column.reset_positions()
            manager_column.update_content([empty_message])

    def resize(self, width, height):
        scroll_vs_position = self.focused.get_position() - self.focused_column.scrolled
        if scroll_vs_position > self.ui.height-4:
            self.focused_column.scroll(scroll_vs_position - (self.ui.height-4))


    def move_up(self):
        """Will move position up on focused file manager and scroll if necessary"""
        self.focused_column.unmark_position(self.focused.get_position())
        self.focused.move_up()
        self.focused_column.mark_position(self.focused.get_position())
        if self.focused.get_position() < self.focused_column.scrolled:
            self.focused_column.scroll(-1)

    def move_down(self):
        """Will move position down on focused file manager and scroll if necessary"""
        if self.focused.get_position() < len(self.focused.listdir())-1:
            self.focused_column.unmark_position(self.focused.get_position())
            self.focused.move_down()
            self.focused_column.mark_position(self.focused.get_position())
            if self.focused.get_position() - self.focused_column.scrolled > self.ui.height-4:
                # magic number 4 = combined height of title bar + status bar
                self.focused_column.scroll(1)

    def cd_out(self):
        """Will move into parent directory on focused file manager"""
        success = self.focused.cd_out()
        if success:
            self.update_file_list()
            scroll_vs_position = self.focused.get_position() - self.focused_column.scrolled 
            if scroll_vs_position > self.ui.height-4:
                self.focused_column.scroll(scroll_vs_position - (self.ui.height-4))

            self.ui.clear_status_bar()

    def cd_in(self):
        """Will move into selected directory on focused file manager"""
        success = self.focused.cd_in()

        if success:
            self.update_file_list()
            self.ui.clear_status_bar()

    def switch(self):
        """Will switch focused file manager, ie switch column"""
        self.ui.clear_status_bar()

        if self.focused == self.adb:
            self.focused = self.fm
            self.focused_column = self.ui.left_column
            self.ui.right_column.unfocus()
            self.ui.left_column.focus()
        else:
            self.focused = self.adb
            self.focused_column = self.ui.right_column
            self.ui.left_column.unfocus()
            self.ui.right_column.focus()

    def transfer(self):
        """Will transfer file or folder from focused device to unfocused device"""
        try:
            if self.focused == self.adb:
                self.adb.pull(self.fm.get_current_path(), lambda out: self.ui.print_status_bar(out))
                self.fm._get_current_folder_content() # private, naughty
                self.update_file_list(manager=self.fm, manager_column=self.ui.left_column)
            else:
                self.adb.push(self.fm.focused_path(), lambda out: self.ui.print_status_bar(out))
                self.update_file_list(manager=self.adb, manager_column=self.ui.right_column)

        except LookupError: # for focused_path()
            self.ui.print_status_bar('No file selected to transfer')

    def letter_input(self, letter):
        """Will filter content in focused column to those beginning with letter"""
        self.focused.filter(letter)
        self.update_file_list(empty_message='--No match--')
        self.ui.print_status_bar('Filtering: {}'.format(self.focused.filter_letters()))

    def backspace(self):
        """Will remove one letter in filter"""
        try:
            self.focused.backstep_filter()
            self.update_file_list()
            self.ui.print_status_bar('Filtering: {}'.format(self.focused.filter_letters()))
        except IndexError:
            self.ui.clear_status_bar()

    def quit(self):
        """Will application"""
        self.ui.quit()



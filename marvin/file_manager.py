# -*- coding: utf-8 -*-
"""
file_manager contains the appropiet functionallity to to
communicate with the local file system
"""

import os
if os.name == 'nt':
    import win32api, win32con

from marvin.content_filterer import ContentFilterer
from marvin.marked_list import MarkedList

class FileManager:
    """Communicates with the local file system"""

    def __init__(self, invisible_files=True):
        """Setup connection with local file system"""
        self.invisible_files = invisible_files
        self.position = 0
        self.position_history = []
        self.permission_denied = False
        self.current_path = os.getcwd()
        self._get_current_folder_content()
        self.filterer = ContentFilterer()

    def listdir(self):
        """Return all content in current directory as a list"""
        return self.folder_content

    def update_listdir(self):
        self._get_current_folder_content()

    def _get_current_folder_content(self):
        """Get all files and folders in the current folder"""
        try:
            dir_content = os.listdir(self.current_path)
            self.permission_denied = False
        except PermissionError:
            self.folder_content = []
            self.permission_denied = True
        else:
            directories = MarkedList()
            files = MarkedList()
            for content in dir_content:
                content_path = os.path.join(self.current_path, content)
                if not self.invisible_files and is_hidden(content_path):
                    continue

                if os.path.isdir(content_path):
                    directories.append(content, marked=True)
                elif os.path.isfile(content_path):
                    files.append(content)

            directories.extend(files)
            self.folder_content = directories
        return self.folder_content

    def get_current_path(self):
        """Return current working directory (cwd/pwd)"""
        return self.current_path

    def current_file(self):
        """Return the name of the currently selected file or folder"""
        if len(self.folder_content) <= self.position:
            raise LookupError('No file exist on position')

        return self.folder_content[self.position]

    def focused_path(self):
        """Return absolute path to the currently selected file or folder"""
        return os.path.join(self.current_path, self.current_file())

    def get_position(self):
        """Return position in folder in form of index (int)"""
        return self.position

    def reset_position(self):
        """Reset postion in folder to 0"""
        self.position = 0

    def move_up(self):
        """Move one position up"""
        self.position = max(self.position-1, 0)

    def move_down(self):
        """Move one position down"""
        self.position = min(self.position+1, len(self.folder_content)-1)

    def cd_in(self):
        """Change directory into the currently selected folder
        Return True if successful, otherwise False
        If the currently selected is not a folder, it will not be successful
        """
        selected_folder = self.current_file()

        next_path = os.path.join(self.current_path, selected_folder)
        if os.path.isdir(next_path):
            self.current_path = next_path
            self._get_current_folder_content()
            self.position_history.append(self.position)
            self.reset_position()
            self.filterer.clear_content()
            return True
        else:
            return False

    def cd_out(self):
        """Change directory into parent directory
        Return True if successful, otherwise False
        """
        self.current_path = os.path.dirname(self.current_path)
        self._get_current_folder_content()
        try:
            self.position = self.position_history.pop()
        except IndexError:
            self.reset_position()
        self.filterer.clear_content()
        return True

    def delete(self):
        """Delete current selected fileor folder on local file system
        (not implemented)"""
        pass

    def toogle_invisible_files(self, show=None):
        """Change state on whether to show invisible files and folders or not
        Will toggle option if argument show is not given, else use what bool show is
        """
        if show:
            self.invisible_files = show
        else:
            self.invisible_files = not self.invisible_files
        self._get_current_folder_content()

    def filter(self, letter):
        """Reduce current folder content to those beginning with given letter
        Multiple calls with be additive
        """
        if not self.filterer.is_initialized():
            self.filterer.set_initial_content(self.folder_content)
        self.folder_content = self.filterer.filter(letter)
        self.reset_position()

    def backstep_filter(self):
        """Return filted content to previus step(letter)"""
        self.folder_content = self.filterer.backstep()
        self.reset_position()

    def filter_letters(self):
        """Return all sequential letters used in filter()"""
        return self.filterer.get_current_filter_letters()



# from: http://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir-python
def is_hidden(path):
    name = os.path.basename(path)
    if os.name== 'nt': # windows
        attribute = win32api.GetFileAttributes(path)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return name.startswith('.') # unix (linux-osx)

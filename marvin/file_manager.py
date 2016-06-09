import os

class FileManager:

    def __init__(self):
        self.position = 0
        self.position_history = []
        self.current_path = os.getcwd()
        self.folder_content = os.listdir(self.current_path)

    def listdir(self):
        return self.folder_content

    def _get_current_folder_content(self):
        self.folder_content = os.listdir(self.current_path)
        return self.folder_content

    def get_current_path(self):
        return self.current_path

    def current_file(self):
        if len(self.folder_content) <= self.position:
            raise LookupError('No file exist on position')

        return self.folder_content[self.position]

    def focused_path(self):
        return os.path.join(self.current_path, self.current_file())

    def get_position(self):
        return self.position

    def reset_position(self):
        self.position = 0

    def move_up(self):
        self.position = max(self.position-1, 0)

    def move_down(self):
        self.position = min(self.position+1, len(self.folder_content)-1)

    def cd_in(self):
        if os.path.isdir(os.path.join(self.current_path, self.current_file())):
            self.current_path = os.path.join(self.current_path, self.current_file())
            self.folder_content = os.listdir(self.current_path)
            self.position_history.append(self.position)
            self.reset_position()
            return True
        else:
            return False

    def cd_out(self):
        self.current_path = os.path.dirname(self.current_path)
        self.folder_content = os.listdir(self.current_path)
        try:
            self.position = self.position_history.pop()
        except IndexError:
            self.reset_position()
        return True
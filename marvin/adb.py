"""
adb contains the appropiet functionallity to use the adb (Android device bride)
command to communicate with a android device, on a file system level
"""

import subprocess
from subprocess import check_output
from os import path

from marvin.file_manager import FileManager
from marvin.content_filterer import ContentFilterer


SDCARD_PATH = '/storage/emulated/0'

class ADBError(Exception):
    """Something has gone wrong while performing a command using adb (Android device bridge)"""

class ADB(FileManager):
    """ADB communicates with the file system on an android device"""

    def __init__(self):
        """Setup, connection with android device"""
        command = ['adb', 'devices']
        output = check_output(command).decode('utf-8')
        output_list = output.split('\n')
        if len(output_list) < 4:
            raise ADBError('No device was found')

        self.position = 0
        self.position_history = []
        self.current_path = SDCARD_PATH
        self.folder_content = []
        self._get_current_folder_content()
        self.filterer = ContentFilterer()

    def _is_device_connected(self):
        """Check if a device is connected"""

        command = ['adb', 'devices']
        output = check_output(command).decode('utf-8')
        output_list = output.split('\n')
        if len(output_list) < 4:
            raise ADBError('Device was disconnected')

    def _get_current_folder_content(self):
        """Get all files and folders in the current folder"""
        
        self._is_device_connected()
        command = ['adb', 'shell', 'cd "{}" && ls -a'.format(self.current_path)]
        output = check_output(command).decode('utf-8')
        output_list = output.split('\r\n')
        try:
            output_list.remove('')
        except:
            pass

        self.folder_content = output_list

    def cd_in(self):
        """Change directory into the currently selected on

        Return True is successful, otherwise, False
        """

        self._is_device_connected()

        selected_folder = self.folder_content[self.position]

        if len(self.folder_content) > self.position and \
                self.is_folder(selected_folder):
            self.current_path = path.join(self.current_path, selected_folder)
            self._get_current_folder_content()
            self.position_history.append(self.position)
            self.reset_position()
            self.filterer.clear_content()
            return True
        else:
            return False

    def cd_out(self):
        """Change directory to the parent directory

        Return True is successful, otherwise, False
        """

        self._is_device_connected()
        if (path.normpath(self.current_path) != SDCARD_PATH):
            self.current_path = path.dirname(self.current_path)
            self._get_current_folder_content()
            self.position = self.position_history.pop()
            self.filterer.clear_content()
            return True
        else:
            return False

    def push(self, file, output_printer):
        """Transfer given file from local device to the current folder of the android device"""

        self._is_device_connected()
        if self.path_exist(path.join(self.current_path, path.basename(file))):
            output_printer('Transfer failed: filename already exist')
        else:
            command = ['adb', 'push', '-p', file, self.current_path]
            try:
                for output in execute(command):
                    output_printer(_remove_newlines(output))
                output_printer('Transfer success ({})'.format(_remove_newlines(output)))
            except KeyboardInterrupt:
                output_printer('Transfer canceled')
            except subprocess.CalledProcessError:
                output_printer('Transfer failed: {}'.format(_remove_newlines(output)))
            self._get_current_folder_content()

    def pull(self, directory, output_printer):
        """Transfer current file from android device to the given directory on local device"""

        self._is_device_connected()
        try:
            if path.exists(path.join(directory, self.current_file())):
                output_printer('Transfer failed: filename already exist')
            else:
                command = ['adb', 'pull', '-p', path.join(self.current_path, self.current_file()), directory]
                try:
                    for output in execute(command):
                        output_printer(_remove_newlines(output))
                    output_printer('Transfer success ({})'.format(_remove_newlines(output)))
                except KeyboardInterrupt:
                    output_printer('Transfer canceled')
                except subprocess.CalledProcessError:
                    output_printer('Transfer failed: {}'.format(_remove_newlines(output)))

        except LookupError: # for self.current_file()
            output_printer('No file selected to transfer')

    def get_device_name(self):
        """Return the model of the android device"""

        command = ['adb', 'devices', '-l']
        output = check_output(command).decode('utf-8')
        output_list = output.split('\n')
        if len(output_list) >= 2:
            device_info = output_list[1]
            start_index = device_info.find('model:') + 6 #len('model:')
            end_index = device_info.find(' ', start_index)
            device_name = device_info[start_index:end_index]
            return device_name
        else:
            raise ADBError('No device was found')

    def path_exist(self, path):
        """Checks if the given path exist on the android device"""

        self._is_device_connected()
        confirmation_string = ': No such file or directory'
        command = ['adb', 'shell', 'cd "{}" && ls "{}"'
                  .format(self.current_path, path)]
        output = check_output(command).decode('utf-8').split('\r\n')[0]
        if confirmation_string in output:
            return False
        else:
            return True

    def is_folder(self, path):
        """Checks if current file on android device is a directory"""

        self._is_device_connected()
        confirmation_string = 'not a file 356896741'
        command = ['adb', 'shell', 'cd {} && [ -d "{}" ] && echo "{}"'
                  .format(self.current_path, path, confirmation_string)]
        output = check_output(command).decode('utf-8').split('\r\n')[0]
        if output == confirmation_string:
            return True
        else:
            return False

    def delete(self):
        """Delete current file on android device (not implemented)"""



# Taken from: http://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
def execute(command):
    """Generator which will perform the given command and yeild the ouput

    Makes it possible to perform actions on the continues output 
    asynchronous to the command running.
    """

    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout_lines = iter(popen.stderr.readline, "")
    for stdout_line in stdout_lines:
        yield stdout_line

    popen.stdout.close()
    returncode =  popen.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, command)


def _remove_newlines(string):
    """Remove all instanzes of \\n and \\r"""
    return string.replace('\n', '').replace('\r', '')



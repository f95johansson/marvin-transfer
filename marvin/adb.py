# -*- coding: utf-8 -*-
"""
adb contains the appropiet functionallity to use the adb (Android device bride)
command to communicate with a android device, on a file system level
"""
from __future__ import unicode_literals
import subprocess
from subprocess import check_output
from os import path
import unicodedata

from marvin.file_manager import FileManager
from marvin.content_filterer import ContentFilterer
from marvin.marked_list import MarkedList


class ADBError(Exception):
    """Something has gone wrong while performing a command using adb (Android device bridge)"""

class ADB(FileManager):
    """ADB communicates with the file system on an android device"""

    def __init__(self, invisible_files=True, adb_path='adb',
                    sdcard_path='/storage/emulated/0'):
        """Setup, connection with android device"""
        command = [adb_path, 'devices']
        output = check_output(command).decode('utf-8')
        output_list = output.split('\n')
        if len(output_list) < 4:
            raise ADBError('No device was found')

        self.invisible_files = invisible_files
        self.adb_path = adb_path
        self.sdcard_path = sdcard_path
        self.position = 0
        self.position_history = []
        self.permission_denied = False
        self.current_path = self.sdcard_path
        self.folder_content = MarkedList()
        self._get_current_folder_content()
        self.filterer = ContentFilterer()

    def _is_device_connected(self):
        """Check if a device is connected"""

        command = [self.adb_path, 'devices']
        output = check_output(command).decode('utf-8')
        output_list = output.split('\n')
        if len(output_list) < 4:
            raise ADBError('Device was disconnected')

    def _get_current_folder_content(self):
        """Get all files and folders in the current folder"""
        
        self._is_device_connected()
        invisble_flag = '-a' if self.invisible_files else ''
        command = [self.adb_path, 'shell', 'ls {} "{}/" && ls {} -l "{}/"'.format(
                    invisble_flag, self.current_path, invisble_flag, self.current_path)]
        output = check_output(command).decode('utf-8')

        if output.endswith('Permission denied\r\n'):
            self.permission_denied = True
            self.folder_content = []
            return
        else:
            self.permission_denied = False
        
        output_list = self._sort_folders_from_files_in_ls(output)
        try:
            output_list.remove('')
        except:
            pass
        self.folder_content = output_list
        return self.folder_content

    def _sort_folders_from_files_in_ls(self, content):
        directories = MarkedList()
        files = MarkedList()

        content_list = content.split('\r\n')
        if content_list[len(content_list)-1] == '':
            content_list.pop()
        length = len(content_list)//2 # content includes both ls and ls -l

        for i, name in enumerate(content_list):
            if i >= length:
                break

            name = unicodedata.normalize('NFC', name) # remove potential decomposed utf-8

            if name != '':
                if content_list[length+i].startswith('d'):
                    directories.append(name, marked=True)
                elif content_list[length+i].startswith('-'):
                    files.append(name)
                elif content_list[length+i].startswith('l'): # symbolic link
                    if self.is_folder(name):
                        directories.append(name, marked=True)
                    else:
                        files.append(name)

        directories.extend(files)
        return directories

    def cd_in(self):
        """Change directory into the currently selected on

        Return True is successful, otherwise, False
        """

        self._is_device_connected()

        try:
            selected_folder = self.folder_content[self.position]
        except IndexError:
            return False


        if self.position < len(self.folder_content) and \
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
        if (path.normpath(self.current_path) != self.sdcard_path):
            self.current_path = path.dirname(self.current_path)
            self._get_current_folder_content()
            self.position = self.position_history.pop()
            self.filterer.clear_content()
            return True
        else:
            return False

    def push(self, file, output_printer):
        """Transfer given file from local device to the current folder of the android device"""

        try:
            self._is_device_connected()
            if self.path_exist(path.join(self.current_path, path.basename(file))):
                output_printer('Transfer failed: filename already exist')
                print('\a') # error noise
            else:
                command = [self.adb_path, 'push', '-p', file, self.current_path]
                try:
                    for output in execute(command):
                        output_printer(_remove_newlines(output))
                    output_printer('Transfer success ({})'.format(_remove_newlines(output)))

                except UnboundLocalError: # no output (happens with empty files)
                    output_printer('Transfer success')
                except KeyboardInterrupt:
                    output_printer('Transfer canceled')
                except subprocess.CalledProcessError:
                    output_printer('Transfer failed: {}'.format(_remove_newlines(output)))
                    print('\a')
                self._get_current_folder_content()

        except UnicodeDecodeError:
            output_printer('Sorry, non-ascii chatacters not supported')
            print('\a')

    def pull(self, directory, output_printer):
        """Transfer current file from android device to the given directory on local device"""

        try:
            self._is_device_connected()
            try:
                if path.exists(path.join(directory, self.current_file())):
                    output_printer('Transfer failed: filename already exist')
                    print('\a')
                else:
                    command = [self.adb_path, 'pull', '-p', path.join(self.current_path, self.current_file()), directory]
                    try:
                        for output in execute(command):
                            output_printer(_remove_newlines(output))
                        output_printer('Transfer success ({})'.format(_remove_newlines(output)))

                    except UnboundLocalError: # no output (happens with empty files)
                        output_printer('Transfer success')
                    except KeyboardInterrupt:
                        output_printer('Transfer canceled')
                    except subprocess.CalledProcessError:
                        output_printer('Transfer failed: {}'.format(_remove_newlines(output)))
                        print('\a')

            except LookupError: # for self.current_file()
                output_printer('No file selected to transfer')
                print('\a')

        except UnicodeDecodeError:
            output_printer('Sorry, non-ascii chatacters not supported')
            print('\a')


    def get_device_name(self):
        """Return the model of the android device"""

        command = [self.adb_path, 'devices', '-l']
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
        command = [self.adb_path, 'shell', 'cd "{}" && ls "{}"'
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
        command = [self.adb_path, 'shell', 'cd {} && [ -d "{}" ] && echo "{}"'
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
    stdout_lines = iter(popen.stderr.readline, '')
    for stdout_line in stdout_lines:
        yield stdout_line

    popen.stdout.close()
    returncode =  popen.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, command)


def _remove_newlines(string):
    """Remove all instanzes of \\n and \\r"""
    return string.replace('\n', '').replace('\r', '')



import subprocess
from subprocess import check_output
from os import path

from marvin.file_manager import FileManager

SDCARD_PATH = '/storage/emulated/0'

class ADBError(Exception):
    pass

class ADB(FileManager):

    def __init__(self):
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

    def _get_current_folder_content(self):
        command = ['adb', 'shell', 'cd "{}" && ls'.format(self.current_path)]
        output = check_output(command).decode('utf-8')
        output_list = output.split('\r\n')
        try:
            output_list.remove('')
        except:
            pass

        self.folder_content = output_list

    def cd_in(self):
        if len(self.folder_content) > self.position and \
                self.is_folder(self.folder_content[self.position]):
            self.current_path = path.join(self.current_path, self.folder_content[self.position])
            self._get_current_folder_content()
            self.position_history.append(self.position)
            self.reset_position()
            return True
        else:
            return False

    def cd_out(self):
        if (path.normpath(self.current_path) != SDCARD_PATH):
            self.current_path = path.dirname(self.current_path)
            self._get_current_folder_content()
            self.position = self.position_history.pop()
            return True
        else:
            return False

    def push(self, file, output_printer):
        if self.path_exist(path.join(self.current_path, path.basename(file))):
            output_printer('Transfer failed: filename already exist')
        else:
            command = ['adb', 'push', '-p', file, self.current_path]
            try:
                for output in execute(command):
                    output_printer(output)
                output_printer('Transfer success ({})'.format(output))
            except subprocess.CalledProcessError:
                output_printer('Transfer failed: {}'.format(output))
            self._get_current_folder_content()

    def pull(self, directory, output_printer):
        if path.exists(path.join(directory, self.current_file())):
            output_printer('Transfer failed: filename already exist')
        else:
            command = ['adb', 'pull', '-p', path.join(self.current_path, self.current_file()), directory]
            try:
                for output in execute(command):
                    output_printer(output)
                output_printer('Transfer success ({})'.format(output))
            except subprocess.CalledProcessError:
                output_printer('Transfer failed: {}'.format(output))

    def get_device_name(self):
        command = ['adb', 'devices', '-l']
        output = check_output(command).decode('utf-8')
        output_list = output.split('\n')
        if len(output_list) >= 2:
            device_info = output_list[1]
            device_name = device_info.split(' ')[14].replace('model:', '')
            return device_name
        else:
            raise ADBError('No device was found')

    def path_exist(self, path):
        confirmation_string = ': No such file or directory'
        command = ['adb', 'shell', 'cd {} && ls "{}"'
                  .format(self.current_path, path)]
        output = check_output(command).decode('utf-8').split('\r\n')[0]
        if confirmation_string in output:
            return False
        else:
            return True

    def is_folder(self, path):
        confirmation_string = 'not a file 356896741'
        command = ['adb', 'shell', 'cd {} && [ -d "{}" ] && echo "{}"'
                  .format(self.current_path, path, confirmation_string)]
        output = check_output(command).decode('utf-8').split('\r\n')[0]
        if output == confirmation_string:
            return True
        else:
            return False



# Taken from: http://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
def execute(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout_lines = iter(popen.stderr.readline, "")
    for stdout_line in stdout_lines:
        yield stdout_line

    popen.stdout.close()
    returncode =  popen.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, command)


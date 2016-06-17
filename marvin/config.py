# -*- coding: utf-8 -*-
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os

import marvin.appdirs as appdirs

# Preferences:
#  * adb path
#  * invisible files & folders
#  * android root directory

class _Options:
    def __init__(self):
        self._options = {
            'ADB_PATH': str,
            'INVISIBLE': bool,
            'SDCARD_PATH': str
        }
        for key in self._options:
            self.__setattr__(key, key)

    def __getitem__(self, key):
        pass

    def __contains__(self, key):
        return key in self._options

    def __str__(self):
        return str(self._options)

class Config:
    options = {
        'ADB_PATH': str,
        'INVISIBLE': bool,
        'SDCARD_PATH': str
    }

    __doc__ = """
    Keys must be one of the following, values must
    be of the class corresponding to key:
    """+str(options)

    def __init__(self, app_name):
        self._app_name = app_name
        self._config_dir_path = appdirs.user_config_dir(appname=app_name)
        self._config_file_path = os.path.join(self._config_dir_path, 'preferences.conf')
        self._configparser = configparser.ConfigParser()
        self._configparser.read(self._config_file_path)
        self._section = 'DEFAULT'

    def __getitem__(self, key):
        key = str(key)
        if key not in self.options:
            raise ValueError('Invalid key')

        try:
            if self.options[key] == float:
                return self._configparser.getfloat(self._section, key)
            elif self.options[key] == int:
                return self._configparser.getint(self._section, key)
            elif self.options[key] == bool:
                return self._configparser.getboolean(self._section, key)
            else:
                return self._configparser.get(self._section, key)
        except KeyError:
            return None
        except ValueError as e:
            raise e

    def __setitem__(self, key, value):
        key = str(key)
        if key in Config.options:
            if type(value) != Config.options[key]:
                raise ValueError('Value of wrong type. '+ 
                    'See help(Config) for correct types for keys')
            self._configparser.set(self._section, key, str(value))
            self._write_to_file()
        else:
            raise KeyError('Invalid key')

    def __delitem__(self, key):
        self._configparser.remove_option(self._section, key)
        self._write_to_file()

    def __contains__(self, key):
        return self._configparser.has_option(self._section, key)

    def __str__(self):
        return ''.join(['{}: {}\n'.format(option, self._configparser.get(self._section, option))
                    for option in self._configparser[self._section]])

    def _write_to_file(self):
        try: 
            os.makedirs(self._config_dir_path)
        except OSError:
            if not os.path.isdir(self._config_dir_path):
                raise OSError('Config directory is not a directory')

        with open(self._config_file_path, 'w') as f:
            self._configparser.write(f)
            f.close()

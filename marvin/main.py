# -*- coding: utf-8 -*-
"""main takes care of the upstart of the program"""

import sys
import argparse

from marvin import ui
from marvin.app import App
from marvin.adb import ADBError
from marvin.config import Config

import locale # for python 2.7, to set encoding to utf-8 in curses
locale.setlocale(locale.LC_ALL, '')

def parser(config):
    """Parse all the arguments given from command line"""
    args = sys.argv[1:]
    if '-h' in args or '-help' in args or '--help' in args:
        print_help()
        return False

    if '--show-invisible' in args:
        index = args.index('--show-invisible')
        try:
            next_arg =  args[index+1]
        except IndexError:
            print('Wrong arguments\n')
            print_help()
            return False
        else:
            if next_arg in ['True', 'true', '1', 'yes']:
                config['INVISIBLE'] = True
            elif next_arg in ['False', 'false', '0', 'no']:
                config['INVISIBLE'] = False
            else:
                print('Wrong arguments\n')
                print_help()
                return False

    if '--sdcard-path' in args:
        index = args.index('--sdcard-path')
        try:
            next_arg =  args[index+1]
        except IndexError:
            print('Wrong arguments\n')
            print_help()
            return False
        else:
            if next_arg.startswith('--') or next_arg.startswith('-'):
                print('Wrong arguments\n')
                print_help()
                return False
            else:
                config['SDCARD_PATH'] = next_arg

    if '--adb-path' in args:
        index = args.index('---adb-path')
        try:
            next_arg =  args[index+1]
        except IndexError:
            print('Wrong arguments\n')
            print_help()
            return False
        else:
            if next_arg.startswith('--') or next_arg.startswith('-'):
                print('Wrong arguments\n')
                print_help()
                return False
            else:
                config['SDCARD_PATH'] = next_arg

    return True

 
def print_help():
    """Print instructions on how to use this program"""
    print(
    ("Marvin transfer 0.3.0\n"
    "To easily transfer file and folder between android device and computer\n"
    "\n"
    "UI Usage:\n"
    "  Use arrow keys to navigate (right/left to enter/exit folders)\n"
    "  <enter> to transfer currently selected file/foder\n"
    "  <tab>/<space> to change focus between local computer and android device\n"
    "  <escape>/<ctrl-c> to exit program\n""  typing letters works as a filter on the current directory, for faster navigation\n"
    "  <ctrl-t> Show/hide invisible files/folders (remains after shutdown of utility)"
    "\n"
    "Settings:\n"
    "  Use these arguments to set preferences which will remain after shutdown\n"
    "  --show-invisible <true/false> - Whether to show invisible files/folders or not\n"
    "  --sdcard-path <string> - Set path to interval or external storage. Defaults to /storage/emulated/0, but may be different across android devices\n"
    "  --adb-path <string> - If adb is not in $PATH, you can set it manually\n"
    "\n")
    )


def main():
    """Main function, starts the application with the ui"""
    config = Config('marvin-transfer')
    ok_to_continue = parser(config)

    if ok_to_continue:
        try:
            application = App(config=config)
            ui.run(application.start)
            print('Exiting')

        except KeyboardInterrupt:
            print('Exiting')

        except ADBError as e:
            print('Adb error: {}'.format(e))

        except ui.UIError:
            print('An UI error occurd')



if __name__ == '__main__':
    main()

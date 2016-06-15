# -*- coding: utf-8 -*-
"""main takes care of the upstart of the program"""

import sys

from marvin import ui
from marvin.app import App
from marvin.adb import ADBError

import locale # for python 2.7, to set encoding to utf-8 in curses
locale.setlocale(locale.LC_ALL, '')

def parser():
    """Parse all the arguments given from command line"""
    args = sys.argv[1:]
    if '-h' in args or '-help' in args or '--help' in args:
        print_help()
        return False

    return True
 
def print_help():
    """Print instructions on how to use this program"""
    print(
    ("Marvin transfer 0.2\n"
    "To easily transfer file and folder between android device and computer\n"
    "\n"
    "Usage:\n"
    "  Use arrow keys to navigate (right/left to enter/exit folders)\n"
    "  <enter> to transfer currently selected file/foder\n"
    "  <tab>/<space> to change focus between local computer and android device\n"
    "  <escape>/<ctrl-c> to exit program\n""  typing letters works as a filter on the current directory, for faster navigation\n"
    "\n")
    )

def main():
    """Main function, starts the application with the ui"""
    ok_to_continue = parser()

    if ok_to_continue:
        try:
            application = App()
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

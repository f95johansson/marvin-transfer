#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Marvin transfer 0.4.2

This program uses adb (Android device bridge) to easy
the task of transfering file between a computer and an
Android device. 

UI Usage:
  Use arrow keys to navigate (right/left to enter/exit folders)
  <enter> to transfer currently selected file/folder
  <tab>/<space> to change focus between local computer and android device
  <escape>/<ctrl-c> to exit program
  typing letters works as a filter on the current directory, for faster navigation
  <ctrl-t> Show/hide invisible files/folders (remains after shutdown of utility)

Settings:
  Use these arguments to set preferences which will remain after shutdown
  --show-invisible <true/false> - Whether to show invisible files/folders or not
  --sdcard-path <string> - Set path to interval or external storage. Defaults to /storage/emulated/0, but may be different across android devices
  --adb-path <string> - If adb is not in $PATH, you can set it manually


Copyright (c) 2016 Fredrik Johansson
"""

from marvin.main import main

if __name__ == '__main__':
    main()
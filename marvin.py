#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Marvin transfer 0.3.0

This program uses adb (Android device bridge) to easy
the task of transfering file between a computer and an
Android device. 

Help:
  use arrow keys to navigate (right/left to enter/exit folders)
  <enter> to transfer currently selected file/foder
  <tab>/<space> to change focus between local computer and android device
  <escape>/<ctrl-c> to exit program
  typing letters works as a filter on the current directory, for faster navigation

Copyright (c) 2016 Fredrik Johansson


This module is simply a wrapper for the main function inside marvin package
"""

from marvin.main import main

if __name__ == '__main__':
    main()
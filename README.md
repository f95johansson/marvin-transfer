Marvin transfer
===============
A command line utility for easy file and folder transfer between local computer and android device  

![Marvin demo](marvin-demo.gif)  

Especially on mac transferring files to an android device can be a hassle. The Android File Transfer app is completely useless and setting up a mtp fuse can be unstable. That's why Marvin transfer exist, to ease the pain.  

## Install
### Requirements
* Recommended **Python 3.3 or higher** for full support
* Also works with **Python 2.7** but no promise about future updates
* This utility uses the **ADB (Android Device Bridge)** as a backend and therefor it must be installed and adb must exist in the $PATH or be set with command line argument (see [Settings](#settings))

*(Tested on python3.5/3.3/2.7 on OSX 10.9 with Nexus 5/9 on Android Marshmallow)*


### Clone repository
Clone or download the repository

    git clone https://github.com/f95johansson/marvin-transfer.git

Then you can **try it out** by simply 

    cd marvin-transfer
    python3 marvin.py

**Install** it using python3

    cd marvin-transfer
    pip3 install .

Use `pip` instead of `pip3` if using python2.7

After system wide install, start the application anywhere with

    marvin

### Uninstall
I you decide that you want to uninstall it *(if you installed it with pip3)*

    pip3 uninstall marvin-transfer

Again, `pip` instead of `pip3` if using python2.7



## Usage
The ui consist of two columns, the left one your local computers file system, the right your connected android device's system

* use **arrow keys** to navigate (right/left to enter/exit folders)
* **enter** to transfer currently selected file/folder
* **tab/space** to change focus between local computer and android device
* **escape/ctrl-c** to exit program
* typing letters works as a filter on the current directory, for faster navigation
* **\<ctrl-t\>** Show/hide invisible files/folders (remains after shutdown of utility)

### Settings
Use these arguments to set preferences which will remain after shutdown  
`--show-invisible <true/false>` - Whether to show invisible files/folders or not  
`--sdcard-path <string>` - Set path to interval or external storage. Defaults to /storage/emulated/0, but may be different across android devices  
`--adb-path <string>` - If adb is not in \$PATH, you can set it manually  
*Example:* `marvin --sdcard-path /sdcard/`

## TODO
This utility is quite new and there's a bunch left to be done. Feel free to contribute if you want (with *Pull Requests* targeting *master*). 

* [X] Add help instructions (-h, --help)
* [X] Detect when disconnected
* [X] In list put folders on top (with some distinction)
* [X] Handle resize
* [ ] Add delete option (start with files only)
* [ ] Add make directory option
* [X] Add title bar
* [X] Update file list regularly
* [X] Fast navigation with letters
* [X] Add option for invisible files/folders
* [ ] Visually show cutoffs (of file names etc.)
* [X] Remove requirement for adb in \$PATH
* [X] Add permanent configuration for stuff like invisible files and adb path
* [ ] Add package to PyPi for even easier installation
* [X] Support python 2.7
    * [X] Bunch of unicode fixes
        * [X] declare utf-8 in all files
        * [X] curses get_wchr() not supported (non-ascii entry)
* [X] Extend python 2.7 support beyond ascii (if possible)
* [ ] Add transfer queue system, be able to transfer while navigating


## License
Copyright © 2016 Fredrik Johansson ([fredrik-johansson.com](http://fredrik-johansson.com)).

This software is licensed under GNU GPL v3, see file LICENSE for more details.  
Simply put it, if you decide to distribute this software, please make your source code and changes are public as well, as I have done here. Sharing is caring 😊  

## Change log
2016-19-06 (0.5.0)
> Added full unicode support to python 2.7, emojis and everything 👍

2016-18-06 (0.4.2)
> Re-enabled file list update (non-concurrently, after a few seconds of no input)

2016-18-06 (0.4.1)
> Disabled concurrent file list update (it was not ready yet)
> Added permission checks

2016-17-06 (0.4.0)
> Update file list regularly (concurrently)

2016-17-06 (0.3.0)
> Added settings through arguments

2016-15-06 (0.2.0)
> Support for python 2.7 (only ascii)

2016-11-06 (0.1.0)
>  Initial release

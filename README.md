# Marvin transfer

### TODO

* Detect when disconnected
* Handle resize
* Add delete option (start with files only)
* Add title bar
* Update file list regularly
* Documentation
* Fast navigation with letters √
* (Support python 2.7)
    * Bunch of unicode fixes
        * declare utf-8 in all files
        * curses get_wchr() not supported (non-ascii entry)
        * fix all bytestring.encode('utf-8')
    * in ui.py, ~line 36, ceil/float seems to return floats (?)
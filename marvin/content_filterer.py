# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from marvin.marked_list import MarkedList

class ContentFilterer:
    """ContentFilter filter a list with one letter at a time"""

    def __init__(self, inital_content=None, case_sensitive=False):
        """No content list is necessary for initialization, but many methods
        requires it to be set"""
        self.clear_content()
        self.case_sensitive = case_sensitive
        if inital_content != None:
            self.set_initial_content(inital_content)

    def filter(self, letter):
        """Filter through content for entries beginning with givin letter

        If filter method been called before, the filter will be adative,
        i.e entries beginning with combined filtered letters.
        Letter is suppose to be only of length 1 but is allowed to be
        longer to support surrogate pairs in older python versions
        Returns result
        """

        if len(self._content_history) < 1:
            raise ValueError('No inital content is set')

        current_content = self._content_history[len(self._content_history)-1]
        self._filter_letters.append(letter)
        letters = ''.join(self._filter_letters)
        letters_length = len(letters)
        result = MarkedList()
        for i, entry in enumerate(current_content):
            insert = False
            if self.case_sensitive:
                if entry[:letters_length] == letters:
                    insert = True
            else:
                if entry[:letters_length].lower() == letters.lower():
                    insert = True

            if insert:
                marked = False
                try:
                    if current_content.is_marked(i):
                        marked = True
                except AttributeError:
                    pass # marked = False
                result.append(entry, marked=marked)

        self._content_history.append(result)
        return result

    def backstep(self):
        """Undo previus filter, returns result"""

        if len(self._content_history) > 1:
            self._content_history.pop()
            self._filter_letters.pop()
            return self._content_history[len(self._content_history)-1]
        else:
            raise IndexError('Nothing to backtrack to')

    def get_current_content(self):
        """Return the filtered (if any filter) content""" 
        if len(self._content_history) > 0:
            return self._content_history[len(self._content_history)-1]
        else:
            return []

    def get_current_filter_letters(self):
        """Get the combined letters used in the filters

        Entries from get_current_content() will all begin with the returned letters
        """
        return ''.join(self._filter_letters)

    def set_initial_content(self, content):
        """Set inital content from which the filters should apply to"""
        self.clear_content()
        self._content_history = [content]

    def is_initialized(self):
        """Returns whether initial_content have been provided or not"""
        return len(self._content_history) > 0

    def clear_content(self):
        """Clear a content, initial content and filters"""
        self._content_history = []
        self._filter_letters = []

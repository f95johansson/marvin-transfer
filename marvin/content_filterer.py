
class IllegalArgumentError(ValueError):
    pass

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
        Returns result
        """

        if (len(letter) > 1):
            raise IllegalArgumentError('Letter can only by of length 1')
        if len(self._content_history) < 1:
            raise ValueError('No inital content is set')

        current_content = self._content_history[len(self._content_history)-1]
        letters = self._filter_letters + letter
        letters_length = len(letters)
        result = []
        for entry in current_content:
            if self.case_sensitive:
                if entry[:letters_length] == letters:
                    result.append(entry)
            else:
                if entry[:letters_length].lower() == letters.lower():
                    result.append(entry)
        self._content_history.append(result)
        self._filter_letters += letter
        return result

    def backstep(self):
        """Undo previus filter, returns result"""

        if len(self._content_history) > 1:
            self._content_history.pop()
            self._filter_letters = self._filter_letters[:-1]
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
        return self._filter_letters

    def set_initial_content(self, content):
        """Set inital content from which the filters should apply to"""
        self._content_history = [content]

    def is_initialized(self):
        """Returns whether initial_content have been provided or not"""
        return len(self._content_history) > 0

    def clear_content(self):
        """Clear a content, initial content and filters"""
        self._content_history = []
        self._filter_letters = ''

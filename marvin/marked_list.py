from __future__ import unicode_literals

class MarkedList(list):
    """MarkedList expand the normal list by adding the abbility
    of marking values.
    """

    def __init__(self, *args, **kwargs):
        super(MarkedList, self).__init__(*args, **kwargs)
        self.__marked_values = []

    # extend
    def append(self, value, marked=False):
        """L.append(object, [marked]) -> None -- append object to end
        marked - boolean (default False)
        """
        super(MarkedList, self).append(value)

        self.__marked_values.append(marked)

    # extend
    def extend(self, iterable):
        super(MarkedList, self).extend(iterable)

        if type(iterable) == MarkedList:
            self.__marked_values.extend(iterable.get_all_markings())
        else:
            self.__marked_values.extend([False for i in range(len(iterable))])

    # extend
    def insert(self, index, value, marked=False):
        """L.insert(index, object [marked]) -- insert object before index
        marked - boolean (default False)
        """
        super(MarkedList, self).insert(index, value)
        self.__marked_values.insert(index, marked)

    # extend
    def pop(self, index=None):
        index = index if index != None else len(self)-1
        super(MarkedList, self).pop(index)
        self.__marked_values.pop(index)

    # extend
    def remove(self, value):
        self.__marked_values.pop(self.index(value))
        super(MarkedList, self).remove(value)


    def is_marked(self, index):
        """L.is_marked(index) -> boolean -- return whether value is marked or not
        Raises IndexError if list is empty or index is out of range.
        """
        try:
            return self.__marked_values[index]
        except IndexError:
            return False

    def get_all_markings(self):
        """L.get_all_markings() -> list -- return all markings in form of booleans in a list
        corresponding to the list of with the main values
        """
        return self.__marked_values

    def mark_value(self, index):
        """L.mark_value(index) -> None -- markes the value at index as True
        Raises IndexError if list is empty or index is out of range.
        """
        if index < len(self):
            self.__marked_values[index] = True
        else:
            raise IndexError('list index out of range')

    def unmark_value(self, index):
        """L.unmark_value(index) -> None -- markes the value at index as False
        Raises IndexError if list is empty or index is out of range.
        """
        if index < len(self):
            self.__marked_values[index] = False
        else:
            raise IndexError('list index out of range')





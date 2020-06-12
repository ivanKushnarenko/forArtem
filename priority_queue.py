class _PriorityElement:
    def __init__(self, element, priority):
        self.element = element
        self.priority = float(priority)

    def __eq__(self, other):
        return self.priority == other.priority

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other


class PriorityQueue:
    """ Priority queue that gives values with lower priority first."""
    def __init__(self, data_dict=None):
        if data_dict is None:
            self._data = []
        else:
            for element, priority in data_dict.items():
                self.put(element, priority)

    def empty(self):
        return not len(self._data)

    def put(self, element, priority):
        a = _PriorityElement(element, priority)
        if self.empty():
            self._data.append(a)
        else:
            for i, elem in enumerate(self._data):
                if elem >= a:
                    self._data.insert(i, a)
                    break

    def get(self):
        """ Returns element with lowest priority."""
        if not self:
            raise KeyError('Trying to get element from empty queue')
        return self._data.pop(0).element

    def __bool__(self):
        return not self.empty()


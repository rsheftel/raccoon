import blist

class DataFrame(object):
    def __init__(self, data=None, columns=None, index=None):
        # define from dictionary
        if isinstance(data, dict):
            self._data = [x for x in data.values()]
            self._columns = data.keys()
        if not index:
            self._index = index
    
    def loc(self):
        pass
    
    def iloc(self):
        pass
    
    def at(self, row, column):
        pass

    def columns(self):
        pass
    
    def index(self):
        pass

    def __setitem__(self, index, value):
        pass
    
    def __getitem__(self, index):
        pass
    
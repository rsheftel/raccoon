import blist

class DataFrame(object):
    def __init__(self, data=None, columns=None, index=None):
        # setup the data and column names
        # define from dictionary
        if data is None:
            self._data = [[]]
            if columns:
                # expand to the number of columns
                self._data = self._data * len(columns)
                self._columns = columns
            else:
                self._columns = list()
            if index:
                # pad out to the number of rows
                self._pad_data(max_len = len(index))
                if not columns:
                    self._columns = [1]
        elif isinstance(data, dict):
            self._data = [x for x in data.values()]
            self._columns = list(data.keys())
        
        # TODO: from list of lists. Set columns = 1,2,3 if columns=None, otherwise self._columns = columns assuming right len
        
        # pad the data
        self._pad_data()
        
        # setup index
        self._index = None
        if index:
            self.index = index
        else:
            self.index = list(range(len(self._data[0])))
    
        # sort by columns if provided
        if columns:
            self._sort_columns(columns)
        
    def _sort_columns(self, columns_list):
        if not (all([x in columns_list for x in self._columns]) and all([x in self._columns for x in columns_list])):
            raise AttributeError('columns_list must be all in current columns, and all current columns must be in columns_list')
        new_sort = [self._columns.index(x) for x in columns_list]
        self._data = [self._data[x] for x in new_sort]
        self._columns = [self._columns[x] for x in new_sort]
        
    
    def _pad_data(self, max_len=None):
        if not max_len:
            max_len = max([len(x) for x in self._data])
        for i, col in enumerate(self._data):  # TODO: Can this be an list comprehension
            col.extend([None] * (max_len - len(col)))
        #self.data = [x.extend([None] * (max_len - len(x))) for x in self._data]
    
    def loc(self):
        pass
    
    def iloc(self):
        pass
    
    def at(self, row, column):
        pass

    @property
    def values(self):
        return self._data
        
    @property
    def columns(self):
        # returns a copy
        return self._columns.copy()
        
    @columns.setter
    def columns(self, columns_list):
        if len(columns_list) != len(self.values):
            raise AttributeError('length of columns_list is not the same as the number of columns')
        self._columns = columns_list
    
    @property
    def index(self):
        # returns a copy
        return self._index.copy()
        
    @index.setter
    def index(self, index_list):
        if len(index_list) != len(self.values[0]):
            raise AttributeError('length of index_list must be the same as the length of the data')
        self._index = index_list

    def __setitem__(self, index, value):
        pass
    
    def __getitem__(self, index):
        pass
    
    def to_csv(self, filename):
        pass
    
    def from_csv(self, filename):
        pass
    
    
"""
TODO:
- Index names, need to make an "Index" class to hold this
"""
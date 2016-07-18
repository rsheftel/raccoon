
from itertools import compress
from copy import deepcopy
from collections import OrderedDict


class DataFrame(object):
    def __init__(self, data=None, columns=None, index=None):
        # quality checks
        if (index is not None) and (not isinstance(index, list)):
            raise AttributeError('index must be a list.')
        if (columns is not None) and (not isinstance(columns, list)):
            raise AttributeError('columns must be a list.')

        # standard variable setup
        self._index_name = 'index'

        # define from dictionary
        if data is None:
            self._data = list()
            if columns:
                # expand to the number of columns
                self._data = [[] for x in range(len(columns))]
                self._columns = columns
            else:
                self._columns = list()
            if index:
                if not columns:
                    raise AttributeError('cannot initialize with index but no columns')
                # pad out to the number of rows
                self._index = index
                self._pad_data(max_len=len(index))
            else:
                self._index = list()
        elif isinstance(data, dict):
            # set data from dict values. If dict value is not a list, wrap it to make a single element list
            self._data = [x if isinstance(x, list) else [x] for x in data.values()]
            # setup columns from directory keys
            self._columns = list(data.keys())
            # pad the data
            self._pad_data()
            # setup index
            if index:
                self.index = index
            else:
                self.index = list(range(len(self._data[0])))

        # sort by columns if provided
        if columns:
            self._sort_columns(columns)

    def _sort_columns(self, columns_list):
        if not (all([x in columns_list for x in self._columns]) and all([x in self._columns for x in columns_list])):
            raise AttributeError(
                'columns_list must be all in current columns, and all current columns must be in columns_list')
        new_sort = [self._columns.index(x) for x in columns_list]
        self._data = [self._data[x] for x in new_sort]
        self._columns = [self._columns[x] for x in new_sort]

    def _pad_data(self, max_len=None):
        if not max_len:
            max_len = max([len(x) for x in self._data])
        for i, col in enumerate(self._data):
            col.extend([None] * (max_len - len(col)))

    @property
    def data(self):
        return deepcopy(self._data)

    @property
    def columns(self):
        return self._columns.copy()

    @columns.setter
    def columns(self, columns_list):
        if len(columns_list) != len(self._data):
            raise AttributeError('length of columns_list is not the same as the number of columns')
        self._columns = columns_list

    @property
    def index(self):
        return self._index.copy()

    @index.setter
    def index(self, index_list):
        if len(index_list) != len(self._data[0]):
            raise AttributeError('length of index_list must be the same as the length of the data')
        self._index = index_list

    @property
    def index_name(self):
        return self._index_name

    @index_name.setter
    def index_name(self, name):
        self._index_name = name

    def get(self, indexes=None, columns=None):
        # returns a copy
        # If one value for either indexes or columns then return list, otherwise list of list
        if indexes is None:
            indexes = [True] * len(self._index)
        if columns is None:
            columns = [True] * len(self._columns)
        # singe index and column
        if isinstance(indexes, list) and isinstance(columns, list):
            return self.get_matrix(indexes, columns)
        elif isinstance(indexes, list) and (not isinstance(columns, list)):
            return self.get_rows(indexes, columns)
        elif (not isinstance(indexes, list)) and isinstance(columns, list):
            return self.get_columns(indexes, columns)
        else:
            return self.get_cell(indexes, columns)

    def get_cell(self, index, column):
        i = self._index.index(index)
        c = self._columns.index(column)
        return self._data[c][i]

    def get_rows(self, indexes, column):
        if len(indexes) != (indexes.count(True) + indexes.count(False)):  # index list
            indexes = [x in indexes for x in self._index]  # Look to change to a list of False and just add True
        c = self._columns.index(column)
        return DataFrame(data={column: list(compress(self._data[c], indexes))},
                         index=list(compress(self._index, indexes)))

    def get_columns(self, index, columns):
        data = dict()
        if len(columns) == (columns.count(True) + columns.count(False)):
            columns = list(compress(self._columns, columns))
        for column in columns:
            data[column] = [self.get_cell(index, column)]
        return DataFrame(data=data, index=[index], columns=columns)

    def get_matrix(self, indexes, columns):
        if len(indexes) == (indexes.count(True) + indexes.count(False)):  # boolean list
            i = indexes
            indexes = list(compress(self._index, indexes))
        else:  # index list
            i = [x in indexes for x in self._index]  # Look to change to a list of False and just add True

        if len(columns) == (columns.count(True) + columns.count(False)):  # boolean list
            c = columns
            columns = list(compress(self._columns, columns))
        else:  # name list
            c = [x in columns for x in self._columns]

        data_dict = dict()
        data = list(compress(self._data, c))
        for x, column in enumerate(columns):
            data_dict[column] = list(compress(data[x], i))

        return DataFrame(data=data_dict, index=indexes, columns=columns)

    def _add_row(self, index):
        self._index.append(index)
        for c, col in enumerate(self._columns):
            self._data[c].append(None)

    def _add_missing_rows(self, indexes):
        new_indexes = [x for x in indexes if x not in self._index]
        for x in new_indexes:
            self._add_row(x)

    def _add_column(self, column):
        self._columns.append(column)
        self._data.append([None] * len(self._index))

    def set(self, index=None, column=None, values=None):
        if (index is not None) and (column is not None):
            if isinstance(index, list):
                self.set_column(index, column, values)
            else:
                self.set_cell(index, column, values)
        elif (index is not None) and (column is None):
            self.set_row(index, values)
        elif (index is None) and (column is not None):
            self.set_column(index, column, values)
        else:
            raise AttributeError('either or both of index or column must be provided')

    def set_cell(self, index, column, values):
        try:
            i = self._index.index(index)
        except ValueError:
            i = len(self._index)
            self._add_row(index)
        try:
            c = self._columns.index(column)
        except ValueError:
            c = len(self._columns)
            self._add_column(column)
        self._data[c][i] = values

    def set_row(self, index, values):
        try:
            i = self._index.index(index)
        except ValueError:  # new row
            i = len(self._index)
            self._add_row(index)
        if isinstance(values, dict):
            if not (set(values.keys()).issubset(self._columns)):
                raise AttributeError('keys of values are not all in existing columns')
            for c, column in enumerate(self._columns):
                self._data[c][i] = values.get(column, self._data[c][i])
        else:
            raise AttributeError('cannot handle values of this type.')

    def set_column(self, index=None, column=None, values=None):
        try:
            c = self._columns.index(column)
        except ValueError:  # new column
            c = len(self.columns)
            self._add_column(column)
        if index:  # index was provided
            if not isinstance(values, list):  # single value provided, not a list, so turn values into list
                values = [values for x in index]
            if len(index) == (index.count(True) + index.count(False)):  # boolean list
                if len(index) != len(self._index):
                    raise AttributeError('boolean index list must be same size of existing index')
                if len(values) != index.count(True):
                    raise AttributeError('length of values list must equal number of True entries in index list')
                indexes = [i for i, x in enumerate(index) if x]
                for x, i in enumerate(indexes):
                    self._data[c][i] = values[x]
            else:  # list of index
                if len(values) != len(index):
                    raise AttributeError('length of values and index must be the same.')
                try:  # all index in current index
                    indexes = [self._index.index(x) for x in index]
                except ValueError:  # new rows need to be added
                    self._add_missing_rows(index)
                    indexes = [self._index.index(x) for x in index]
                for x, i in enumerate(indexes):
                    self._data[c][i] = values[x]
        else:  # no index, only values
            if not isinstance(values, list):  # values not a list, turn into one of length same as index
                values = [values for x in self._index]
            if len(values) < len(self._index):
                raise AttributeError('values list must be at least as long as current index length.')
            elif len(values) > len(self._index):
                self._data[c] = values
                self._pad_data()
            else:
                self._data[c] = values

    def _slice_index(self, slicer):
        try:
            start_index = self._index.index(slicer.start)
        except ValueError:
            raise ValueError('start of slice not in the index')
        try:
            end_index = self._index.index(slicer.stop)
        except ValueError:
            raise ValueError('end of slice not in the index')
        if end_index < start_index:
            raise ValueError('end of slice is before start of slice')

        pre_list = [False] * start_index
        mid_list = [True] * (end_index - start_index + 1)
        post_list = [False] * (len(self._index) - 1 - end_index)

        pre_list.extend(mid_list)
        pre_list.extend(post_list)
        return pre_list

    def __getitem__(self, index):
        """
        Usage...
        df['a'] -- get column
        df[['a','b',c']] -- get columns
        df[5, 'b']  -- get cell at index=5, column='b'
        df[[4, 5], 'c'] -- get indexes=[4, 5], column='b'
        df[[4, 5,], ['a', 'b']]  -- get indexes=[4, 5], columns=['a', 'b']

        can also use a boolean list for anyting
        :param index:
        :return:
        """
        if isinstance(index, tuple):  # index and column
            indexes = self._slice_index(index[0]) if isinstance(index[0], slice) else index[0]
            return self.get(indexes=indexes, columns=index[1])
        if isinstance(index, slice):  # just a slice of index
            return self.get(indexes=self._slice_index(index))
        else:  # just the columns
            return self.get(columns=index)

    def __setitem__(self, index, value):
        """
        Usage...

        df[1, 'a'] -- set cell at index=1, column=a
        df[[0, 3], 'b'] -- set index=[0, 3], column=b
        df[1:2, 'b'] -- set index slice 1:2, column=b

        :param index:
        :param value:
        :return:
        """
        if isinstance(index, tuple):  # index and column
            indexes = self._slice_index(index[0]) if isinstance(index[0], slice) else index[0]
            return self.set(index=indexes, column=index[1], values=value)
        if isinstance(index, slice):  # just a slice of index
            return self.set(index=self._slice_index(index), column=None, values=value)
        else:  # just the columns
            return self.set(index=None, column=index, values=value)

    def to_list(self):
        # works for single column only
        if len(self._columns) > 1:
            raise AttributeError('tolist() only works with a single column DataFrame')
        return self._data[0]

    def to_dict(self, index=True, ordered=False):
        # returns column names : [column values]
        result = OrderedDict() if ordered else dict()
        if index:
            result.update({self._index_name: self._index})
        if ordered:
            data_dict = [(column, self._data[i]) for i, column in enumerate(self._columns)]
        else:
            data_dict = {column: self._data[i] for i, column in enumerate(self._columns)}
        result.update(data_dict)
        return result

    def rename_columns(self, rename_dict):
        if not all([x in self._columns for x in rename_dict.keys()]):
            raise AttributeError('all dictionary keys must be in current columns')
        for current in rename_dict.keys():
            self._columns[self._columns.index(current)] = rename_dict[current]

    def head(self, rows):
        rows_bool = [True] * min(rows, len(self._index))
        rows_bool.extend([False] * max(0, len(self._index) - rows))
        return self.get(indexes=rows_bool)

    def tail(self, rows):
        rows_bool = [False] * max(0, len(self._index) - rows)
        rows_bool.extend([True] * min(rows, len(self._index)))
        return self.get(indexes=rows_bool)

    def delete_rows(self, indexes):
        indexes = [indexes] if not isinstance(indexes, list) else indexes
        if len(indexes) == (indexes.count(True) + indexes.count(False)):  # boolean list
            if len(indexes) != len(self._index):
                raise AttributeError('boolean indexes list must be same size of existing indexes')
            indexes = [i for i, x in enumerate(indexes) if x]
        else:
            indexes = [self._index.index(x) for x in indexes]
        indexes = sorted(indexes, reverse=True)  # need to sort and reverse list so deleting works
        for c, column in enumerate(self._columns):
            for i in indexes:
                del self._data[c][i]
        # now remove from index
        for i in indexes:
            del self._index[i]

    def delete_columns(self, columns):
        columns = [columns] if not isinstance(columns, list) else columns
        if not all([x in self._columns for x in columns]):
            raise AttributeError('all columns must be in current columns')
        for column in columns:
            c = self._columns.index(column)
            del self._data[c]
            del self._columns[c]
        if not len(self._data):  # if all the columns have been deleted, remove index
            self._index = list()

    def to_pandas(self):
        # just return a dict of index, columns, data (view not copy)
        pass

    def from_pandas(self):
        pass

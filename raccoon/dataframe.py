"""
DataFrame class
"""
from __future__ import print_function
import sys
from itertools import compress
from collections import OrderedDict, namedtuple
from bisect import bisect_left, bisect_right
from tabulate import tabulate
from blist import blist

PYTHON3 = (sys.version_info >= (3, 0))

try:
    import simplejson as json
except ImportError:
    import json


def sorted_exists(values, x):
    """
    For list, values, returns the insert position for item x and whether the item already exists in the list. This
    allows one function call to return either the index to overwrite an existing value in the list, or the index to
    insert a new item in the list and keep the list in sorted order.

    :param values: list
    :param x: item
    :return: (exists, index) tuple
    """
    i = bisect_left(values, x)
    j = bisect_right(values, x)
    exists = x in values[i:j]
    return exists, i


def sorted_index(values, x):
    """
    For list, values, returns the index location of element x. If x does not exist will raise an error.

    :param values: list
    :param x: item
    :return: integer index
    """
    i = bisect_left(values, x)
    j = bisect_right(values, x)
    return values[i:j].index(x) + i


class DataFrame(object):
    """
    DataFrame class. The raccoon DataFrame implements a simplified version of the pandas DataFrame with the key
    objective difference that the raccoon DataFrame is meant for use cases where the size of the DataFrame rows is
    expanding frequently. This is known to be slow with Pandas due to the use of numpy as the underlying data structure.
    Raccoon uses BList as the underlying data structure which is quick to expand and grow the size. The DataFrame can
    be designated as sorted, in which case the rows will be sorted by index on construction, and then any addition of a
    new row will insert it into the DataFrame so that the index remains sorted.
    """
    def __init__(self, data=None, columns=None, index=None, index_name='index', use_blist=False, sorted=None):
        """
        :param data: (optional) dictionary of lists. The keys of the dictionary will be used for the column names and\
        the lists will be used for the column data.
        :param columns: (optional) list of column names that will define the order
        :param index: (optional) list of index values. If None then the index will be integers starting with zero
        :param index_name: (optional) name for the index. Default is "index"
        :param use_blist: if True then use blist() as the underlying data structure, if False use standard list()
        :param sorted: if True then DataFrame will keep the index sorted. If True all index values must be of same type
        """
        # quality checks
        if (index is not None) and (not isinstance(index, (list, blist))):
            raise TypeError('index must be a list.')
        if (columns is not None) and (not isinstance(columns, (list, blist))):
            raise TypeError('columns must be a list.')

        # standard variable setup
        self._index = None
        self._index_name = index_name
        self._columns = None
        self._blist = use_blist

        # define from dictionary
        if data is None:
            self._data = blist() if self._blist else list()
            if columns:
                # expand to the number of columns
                self._data = blist([blist() for x in range(len(columns))]) if self._blist \
                    else [[] for x in range(len(columns))]
                self.columns = columns
            else:
                self.columns = list()
            if index:
                if not columns:
                    raise ValueError('cannot initialize with index but no columns')
                # pad out to the number of rows
                self._pad_data(max_len=len(index))
                self.index = index
            else:
                self.index = list()
        elif isinstance(data, dict):
            # set data from dict values. If dict value is not a list, wrap it to make a single element list
            self._data = blist([blist(x) if isinstance(x, (list, blist)) else blist([x]) for x in data.values()]) if \
                self._blist else [x if isinstance(x, (list, blist)) else [x] for x in data.values()]
            # setup columns from directory keys
            self.columns = data.keys()
            # pad the data
            self._pad_data()
            # setup index
            if index:
                self.index = index
            else:
                self.index = range(len(self._data[0]))
        else:
            raise TypeError('Not valid data type.')

        # sort by columns if provided
        if columns:
            self._sort_columns(columns)

        # setup sorted
        self._sorted = None
        if sorted is not None:
            self.sorted = sorted
        else:
            if index:
                self.sorted = False
            else:
                self.sorted = True

    def __repr__(self):
        return 'object id: %s\ncolumns:\n%s\ndata:\n%s\nindex:\n%s\n' % (id(self), self._columns,
                                                                         self._data, self._index)

    def __str__(self):
        return self._make_table()

    def _make_table(self, index=True, **kwargs):
        kwargs['headers'] = 'keys' if 'headers' not in kwargs.keys() else kwargs['headers']
        return tabulate(self.to_dict(ordered=True, index=index), **kwargs)

    def show(self, index=True, **kwargs):
        """
        Print the contents of the DataFrame. This method uses the tabulate function from the tabulate package. Use the
        kwargs to pass along any arguments to the tabulate function.

        :param index: If True then include the indexes as a column in the output, if False ignore the index
        :param kwargs: Parameters to pass along to the tabulate function
        :return: output of the tabulate function
        """
        print(self._make_table(index=index, **kwargs))

    def _sort_columns(self, columns_list):
        """
        Given a list of column names will sort the DataFrame columns to match the given order

        :param columns_list: list of column names. Must include all column names
        :return: nothing
        """
        if not (all([x in columns_list for x in self._columns]) and all([x in self._columns for x in columns_list])):
            raise ValueError(
                'columns_list must be all in current columns, and all current columns must be in columns_list')
        new_sort = [self._columns.index(x) for x in columns_list]
        self._data = blist([self._data[x] for x in new_sort]) if self._blist else [self._data[x] for x in new_sort]
        self._columns = blist([self._columns[x] for x in new_sort]) if self._blist \
            else [self._columns[x] for x in new_sort]

    def _pad_data(self, max_len=None):
        """
        Pad the data in DataFrame with [None} to ensure that all columns have the same length.

        :param max_len: If provided will extend all columns to this length, if not then will use the longest column
        :return: nothing
        """
        if not max_len:
            max_len = max([len(x) for x in self._data])
        for i, col in enumerate(self._data):
            col.extend([None] * (max_len - len(col)))

    def __len__(self):
        return len(self._index)

    @property
    def data(self):
        if PYTHON3:
            return self._data.copy()
        else:
            return self._data[:]

    @property
    def columns(self):
        if PYTHON3:
            return self._columns.copy()
        else:
            return self._columns[:]

    @columns.setter
    def columns(self, columns_list):
        self._validate_columns(columns_list)
        self._columns = blist(columns_list) if self._blist else list(columns_list)

    @property
    def index(self):
        if PYTHON3:
            return self._index.copy()
        else:
            return self._index[:]

    @index.setter
    def index(self, index_list):
        self._validate_index(index_list)
        self._index = blist(index_list) if self._blist else list(index_list)

    @property
    def index_name(self):
        return self._index_name

    @index_name.setter
    def index_name(self, name):
        self._index_name = name

    @property
    def blist(self):
        return self._blist

    @property
    def sorted(self):
        return self._sorted

    @sorted.setter
    def sorted(self, boolean):
        self._sorted = boolean
        if self._sorted:
            self.sort_index()

    def select_index(self, compare, result='boolean'):
        """
        Finds the elements in the index that match the compare parameter and returns either a list of the values that
        match, of a boolean list the length of the index with True to each index that matches. If the indexes are
        tuples then the compare is a tuple where None in any field of the tuple will be treated as "*" and match all
        values.

        :param compare: value to compare as a singleton or tuple
        :param result: 'boolean' = returns a list of booleans, 'value' = returns a list of index values that match
        :return: list of booleans or values
        """
        if isinstance(compare, tuple):
            # this crazy list comprehension will match all the tuples in the list with None being an * wildcard
            booleans = [all([(compare[i] == w if compare[i] is not None else True) for i, w in enumerate(v)])
                        for x, v in enumerate(self._index)]
        else:
            booleans = [False] * len(self._index)
            if self._blist:
                booleans[sorted_index(self._index, compare)] = True
            else:
                booleans[self._index.index(compare)] = True
        if result == 'boolean':
            return booleans
        elif result == 'value':
            return list(compress(self._index, booleans))
        else:
            raise ValueError('only valid values for result parameter are: boolean or value.')

    def get(self, indexes=None, columns=None, as_list=False, as_dict=False):
        """
        Given indexes and columns will return a sub-set of the DataFrame. This method will direct to the below methods
        based on what types are passed in for the indexes and columns. The type of the return is determined by the
        types of the parameters.

        :param indexes: index value, list of index values, or a list of booleans. If None then all indexes are used
        :param columns: column name or list of column names. If None then all columns are used
        :param as_list: if True then return the values as a list, if False return a DataFrame. This is only used if
            the get is for a single column
        :param as_dict: if True then return the values as a dictionary, if False return a DataFrame. This is only used
            if the get is for a single row
        :return: either DataFrame, list, dict or single value. The return is a shallow copy
        """
        if (indexes is None) and (columns is not None) and (not isinstance(columns, (list, blist))):
            return self.get_entire_column(columns, as_list)

        if indexes is None:
            indexes = [True] * len(self._index)
        if columns is None:
            columns = [True] * len(self._columns)

        if isinstance(indexes, (list, blist)) and isinstance(columns, (list, blist)):
            return self.get_matrix(indexes, columns)
        elif isinstance(indexes, (list, blist)) and (not isinstance(columns, (list, blist))):
            return self.get_rows(indexes, columns, as_list)
        elif (not isinstance(indexes, (list, blist))) and isinstance(columns, (list, blist)):
            return self.get_columns(indexes, columns, as_dict)
        else:
            return self.get_cell(indexes, columns)

    def get_cell(self, index, column):
        """
        For a single index and column value return the value of the cell

        :param index: index value
        :param column: column name
        :return: value
        """
        i = sorted_index(self._index, index) if self._sorted else self._index.index(index)
        c = self._columns.index(column)
        return self._data[c][i]

    def get_rows(self, indexes, column, as_list=False):
        """
        For a list of indexes and a single column name return the values of the indexes in that column.

        :param indexes: either a list of index values or a list of booleans with same length as all indexes
        :param column: single column name
        :param as_list: if True return a list, if False return DataFrame
        :return: DataFrame is as_list if False, a list if as_list is True
        """
        c = self._columns.index(column)
        if all([isinstance(i, bool) for i in indexes]): # boolean list
            if len(indexes) != len(self._index):
                raise ValueError('boolean index list must be same size of existing index')
            if all(indexes):  # the entire column
                data = self._data[c]
                index = self._index
            else:
                data = list(compress(self._data[c], indexes))
                index = list(compress(self._index, indexes))
        else:  # index values list
            locations = [sorted_index(self._index, x) for x in indexes] if self._sorted \
                else [self._index.index(x) for x in indexes]
            data = [self._data[c][i] for i in locations]
            index = [self._index[i] for i in locations]
        return data if as_list else DataFrame(data={column: data}, index=index, index_name=self._index_name,
                                              sorted=self._sorted)

    def get_columns(self, index, columns, as_dict=False):
        """
        For a single index and list of column names return a DataFrame of the values in that index as either a dict
        or a DataFrame

        :param index: single index value
        :param columns: list of column names
        :param as_dict: if True then return the result as a dictionary
        :return: DataFrame or dictionary
        """
        i = sorted_index(self._index, index) if self._sorted else self._index.index(index)
        return self.get_location(i, columns, as_dict)

    def get_entire_column(self, column, as_list=False):
        """
        Shortcut method to retrieve a single column all rows. Since this is a common use case this method will be
        faster than the more general method.

        :param column: single column name
        :param as_list: if True return a list, if False return DataFrame
        :return: DataFrame is as_list if False, a list if as_list is True
        """
        c = self._columns.index(column)
        data = self._data[c]
        return data if as_list else DataFrame(data={column: data}, index=self._index, index_name=self._index_name,
                                              sorted=self._sorted)

    def get_matrix(self, indexes, columns):
        """
        For a list of indexes and list of columns return a DataFrame of the values.

        :param indexes: either a list of index values or a list of booleans with same length as all indexes
        :param columns: list of column names
        :return: DataFrame
        """
        if all([isinstance(i, bool) for i in indexes]): # boolean list
            is_bool_indexes = True
            if len(indexes) != len(self._index):
                raise ValueError('boolean index list must be same size of existing index')
            bool_indexes = indexes
            indexes = list(compress(self._index, indexes))
        else:
            is_bool_indexes = False
            locations = [sorted_index(self._index, x) for x in indexes] if self._sorted \
                else [self._index.index(x) for x in indexes]

        if all([isinstance(i, bool) for i in columns]): # boolean list
            if len(columns) != len(self._columns):
                raise ValueError('boolean column list must be same size of existing columns')
            columns = list(compress(self._columns, columns))

        col_locations = [self._columns.index(x) for x in columns]
        data_dict = dict()

        for c in col_locations:
            data_dict[self._columns[c]] = list(compress(self._data[c], bool_indexes)) if is_bool_indexes \
                else [self._data[c][i] for i in locations]

        return DataFrame(data=data_dict, index=indexes, columns=columns, index_name=self._index_name,
                         sorted=self._sorted)

    def get_location(self, location, columns=None, as_dict=False, index=True):
        """
        For an index location and list of columns return a DataFrame of the values. This is optimized for speed because
        it does not need to lookup the index location with a search. Also can accept relative indexing from the end of
        the DataFrame in standard python notation [-3, -2, -1]
        
        :param location: index location in standard python form of positive or negative number
        :param columns: list of columns, or None to include all columns
        :param as_dict: if True then return a dictionary
        :param index: if True then include the index in the dictionary if as_dict=True
        :return: DataFrame or dictionary
        """
        if columns is None:
            columns = self._columns
        elif all([isinstance(i, bool) for i in columns]):
            if len(columns) != len(self._columns):
                raise ValueError('boolean column list must be same size of existing columns')
            columns = list(compress(self._columns, columns))
        data = dict()
        for column in columns:
            c = self._columns.index(column)
            data[column] = [self._data[c][location]]
        index_value = self._index[location]
        if as_dict:
            data = {k: data[k][0] for k in data}  # this makes the dict items single values from lists
            if index:
                data[self._index_name] = index_value
            return data
        else:
            return DataFrame(data=data, index=[index_value], columns=columns, index_name=self._index_name,
                             sorted=self._sorted)

    def get_locations(self, locations, columns=None, **kwargs):
        """
        For list of locations and list of columns return a DataFrame of the values.

        :param locations: list of index locations
        :param columns: list of column names
        :param kwargs: will pass along these parameters to the get() method
        :return: DataFrame
        """

        indexes = [self._index[x] for x in locations]
        return self.get(indexes, columns, **kwargs)

    def get_index(self):
        """
        Return a view of the index as a list. Because this is a view any change to the return list from this method
        will corrupt the DataFrame. Use this as view only. This method is proved because copying the index can be an
        expensive operation if you only need to view it.
        
        :return: list 
        """
        return self._index

    def _insert_row(self, i, index):
        """
        Insert a new row in the DataFrame.

        :param i: index location to insert
        :param index: index value to insert into the index list
        :return: nothing
        """
        if i == len(self._index):
            self._add_row(index)
        else:
            self._index.insert(i, index)
            for c in range(len(self._columns)):
                self._data[c].insert(i, None)

    def _insert_missing_rows(self, indexes):
        """
        Given a list of indexes, find all the indexes that are not currently in the DataFrame and make a new row for
        that index, inserting into the index. This requires the DataFrame to be sorted=True

        :param indexes: list of indexes
        :return: nothing
        """
        new_indexes = [x for x in indexes if x not in self._index]
        for x in new_indexes:
            self._insert_row(bisect_left(self._index, x), x)

    def _add_row(self, index):
        """
        Add a new row to the DataFrame

        :param index: index of the new row
        :return: nothing
        """
        self._index.append(index)
        for c, col in enumerate(self._columns):
            self._data[c].append(None)

    def _add_missing_rows(self, indexes):
        """
        Given a list of indexes, find all the indexes that are not currently in the DataFrame and make a new row for
        that index by appending to the DataFrame. This does not maintain sorted order for the index.

        :param indexes: list of indexes
        :return: nothing
        """
        new_indexes = [x for x in indexes if x not in self._index]
        for x in new_indexes:
            self._add_row(x)

    def _add_column(self, column):
        """
        Add a new column to the DataFrame

        :param column: column name
        :return: nothing
        """
        self._columns.append(column)
        if self._blist:
            self._data.append(blist([None] * len(self._index)))
        else:
            self._data.append([None] * len(self._index))

    def set(self, indexes=None, columns=None, values=None):
        """
        Given indexes and columns will set a sub-set of the DataFrame to the values provided. This method will direct
        to the below methods based on what types are passed in for the indexes and columns. If the indexes or columns
        contains values not in the DataFrame then new rows or columns will be added.

        :param indexes: indexes value, list of indexes values, or a list of booleans. If None then all indexes are used
        :param columns: columns name, if None then all columns are used. Currently can only handle a single column or\
        all columns
        :param values: value or list of values to set (index, column) to. If setting just a single row, then must be a\
        dict where the keys are the column names. If a list then must be the same length as the indexes parameter, if\
        indexes=None, then must be the same and length of DataFrame
        :return: nothing
        """
        if (indexes is not None) and (columns is not None):
            if isinstance(indexes, (list, blist)):
                self.set_column(indexes, columns, values)
            else:
                self.set_cell(indexes, columns, values)
        elif (indexes is not None) and (columns is None):
            self.set_row(indexes, values)
        elif (indexes is None) and (columns is not None):
            self.set_column(indexes, columns, values)
        else:
            raise ValueError('either or both of indexes or columns must be provided')

    def set_cell(self, index, column, value):
        """
        Sets the value of a single cell. If the index and/or column is not in the current index/columns then a new
        index and/or column will be created.

        :param index: index value
        :param column: column name
        :param value: value to set
        :return: nothing
        """
        if self._sorted:
            exists, i = sorted_exists(self._index, index)
            if not exists:
                self._insert_row(i, index)
        else:
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
        self._data[c][i] = value

    def set_row(self, index, values):
        """
        Sets the values of the columns in a single row.

        :param index: index value
        :param values: dict with the keys as the column names and the values what to set that column to
        :return: nothing
        """
        if self._sorted:
            exists, i = sorted_exists(self._index, index)
            if not exists:
                self._insert_row(i, index)
        else:
            try:
                i = self._index.index(index)
            except ValueError:  # new row
                i = len(self._index)
                self._add_row(index)
        if isinstance(values, dict):
            if not (set(values.keys()).issubset(self._columns)):
                raise ValueError('keys of values are not all in existing columns')
            for c, column in enumerate(self._columns):
                self._data[c][i] = values.get(column, self._data[c][i])
        else:
            raise TypeError('cannot handle values of this type.')

    def set_column(self, index=None, column=None, values=None):
        """
        Set a column to a single value or list of values. If any of the index values are not in the current indexes
        then a new row will be created.

        :param index: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :param column: column name
        :param values: either a single value or a list. The list must be the same length as the index list if the index\
        list is values, or the length of the True values in the index list if the index list is booleans
        :return: nothing
        """
        try:
            c = self._columns.index(column)
        except ValueError:  # new column
            c = len(self._columns)
            self._add_column(column)
        if index:  # index was provided
            if all([isinstance(i, bool) for i in index]): # boolean list
                if not isinstance(values, (list, blist)):  # single value provided, not a list, so turn values into list
                    values = [values for x in index if x]
                if len(index) != len(self._index):
                    raise ValueError('boolean index list must be same size of existing index')
                if len(values) != index.count(True):
                    raise ValueError('length of values list must equal number of True entries in index list')
                indexes = [i for i, x in enumerate(index) if x]
                for x, i in enumerate(indexes):
                    self._data[c][i] = values[x]
            else:  # list of index
                if not isinstance(values, (list, blist)):  # single value provided, not a list, so turn values into list
                    values = [values for x in index]
                if len(values) != len(index):
                    raise ValueError('length of values and index must be the same.')
                # insert or append indexes as needed
                if self._sorted:
                    exists_tuples = list(zip(*[sorted_exists(self._index, x) for x in index]))
                    exists = exists_tuples[0]
                    indexes = exists_tuples[1]
                    if not all(exists):
                        self._insert_missing_rows(index)
                        indexes = [sorted_index(self._index, x) for x in index]
                else:
                    try:  # all index in current index
                        indexes = [self._index.index(x) for x in index]
                    except ValueError:  # new rows need to be added
                        self._add_missing_rows(index)
                        indexes = [self._index.index(x) for x in index]
                for x, i in enumerate(indexes):
                    self._data[c][i] = values[x]
        else:  # no index, only values
            if not isinstance(values, (list, blist)):  # values not a list, turn into one of length same as index
                values = [values for x in self._index]
            if len(values) != len(self._index):
                raise ValueError('values list must be at same length as current index length.')
            else:
                self._data[c] = blist(values) if self._blist else values

    def set_locations(self, locations, column, values):
        """
        For a list of locations and a column set the values.

        :param locations: list of index locations
        :param column: column name
        :param values: list of values or a single value
        :return: nothing
        """

        indexes = [self._index[x] for x in locations]
        self.set(indexes, column, values)

    def append_row(self, index, values, new_cols=True):
        """
        Appends a row of values to the end of the data. If there are new columns in the values and new_cols is True
        they will be added. Be very careful with this function as it will not test for duplicate indexes and for sorted
        DataFrames it will not enforce sort order. Use this only for speed when needed, be careful.

        :param index: value of the index
        :param values: dictionary of values
        :param new_cols: if True add new columns in values, if False ignore
        :return: nothing
        """

        if new_cols:
            for col in values:
                if col not in self._columns:
                    self._add_column(col)

        # append index value
        self._index.append(index)

        # add data values, if not in values then use None
        for c, col in enumerate(self._columns):
            self._data[c].append(values.get(col, None))

    def _slice_index(self, slicer):
        try:
            start_index = sorted_index(self._index, slicer.start) if self._sorted else self._index.index(slicer.start)
        except ValueError:
            raise IndexError('start of slice not in the index')
        try:
            end_index = sorted_index(self._index, slicer.stop) if self._sorted else self._index.index(slicer.stop)
        except ValueError:
            raise IndexError('end of slice not in the index')
        if end_index < start_index:
            raise IndexError('end of slice is before start of slice')

        pre_list = [False] * start_index
        mid_list = [True] * (end_index - start_index + 1)
        post_list = [False] * (len(self._index) - 1 - end_index)

        pre_list.extend(mid_list)
        pre_list.extend(post_list)
        return pre_list

    def __getitem__(self, index):
        """
        Convenience wrapper around the get() method for using df[]
        Usage...
        df['a'] -- get column
        df[['a','b',c']] -- get columns
        df[5, 'b']  -- get cell at index=5, column='b'
        df[[4, 5], 'c'] -- get indexes=[4, 5], column='b'
        df[[4, 5,], ['a', 'b']]  -- get indexes=[4, 5], columns=['a', 'b']
        can also use a boolean list for anything

        :param index: any of the parameters above
        :return: DataFrame of the subset slice
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
        Convenience wrapper around the set() method for using df[] = X
        Usage...

        df[1, 'a'] -- set cell at index=1, column=a
        df[[0, 3], 'b'] -- set index=[0, 3], column=b
        df[1:2, 'b'] -- set index slice 1:2, column=b

        :param index: any of the parameter examples above
        :param value: single value or list of values
        :return: nothing
        """
        if isinstance(index, tuple):  # index and column
            indexes = self._slice_index(index[0]) if isinstance(index[0], slice) else index[0]
            return self.set(indexes=indexes, columns=index[1], values=value)
        else:  # just the columns
            return self.set(indexes=None, columns=index, values=value)

    def to_list(self):
        """
        For a single column DataFrame returns a list of the values. Raises error if more then one column.

        :return: list
        """
        if len(self._columns) > 1:
            raise TypeError('tolist() only works with a single column DataFrame')
        return self._data[0]

    def to_dict(self, index=True, ordered=False):
        """
        Returns a dict where the keys are the column names and the values are lists of the values for that column.

        :param index: If True then include the index in the dict with the index_name as the key
        :param ordered: If True then return an OrderedDict() to preserve the order of the columns in the DataFrame
        :return: dict or OrderedDict()
        """
        result = OrderedDict() if ordered else dict()
        if index:
            result.update({self._index_name: self._index})
        if ordered:
            data_dict = [(column, self._data[i]) for i, column in enumerate(self._columns)]
        else:
            data_dict = {column: self._data[i] for i, column in enumerate(self._columns)}
        result.update(data_dict)
        return result

    def to_json(self):
        """
        Returns a JSON of the entire DataFrame that can be reconstructed back with raccoon.from_json(input). Any object
        that cannot be serialized will be replaced with the representation of the object using repr(). In that instance
        the DataFrame will have a string representation in place of the object and will not reconstruct exactly.

        :return: json string
        """
        input_dict = {'data': self.to_dict(index=False), 'index': list(self._index)}

        # if blist, turn into lists
        if self.blist:
            input_dict['index'] = list(input_dict['index'])
            for key in input_dict['data']:
                input_dict['data'][key] = list(input_dict['data'][key])

        meta_data = dict()
        for key, value in vars(self).items():
            if key not in ['_data', '_index']:
                meta_data[key.lstrip('_')] = value if not isinstance(value, blist) else list(value)
        meta_data['use_blist'] = meta_data.pop('blist')
        input_dict['meta_data'] = meta_data
        return json.dumps(input_dict, default=repr)

    def rename_columns(self, rename_dict):
        """
        Renames the columns

        :param rename_dict: dict where the keys are the current column names and the values are the new names
        :return: nothing
        """
        if not all([x in self._columns for x in rename_dict.keys()]):
            raise ValueError('all dictionary keys must be in current columns')
        for current in rename_dict.keys():
            self._columns[self._columns.index(current)] = rename_dict[current]

    def head(self, rows):
        """
        Return a DataFrame of the first N rows

        :param rows: number of rows
        :return: DataFrame
        """
        rows_bool = [True] * min(rows, len(self._index))
        rows_bool.extend([False] * max(0, len(self._index) - rows))
        return self.get(indexes=rows_bool)

    def tail(self, rows):
        """
        Return a DataFrame of the last N rows

        :param rows: number of rows
        :return: DataFrame
        """
        rows_bool = [False] * max(0, len(self._index) - rows)
        rows_bool.extend([True] * min(rows, len(self._index)))
        return self.get(indexes=rows_bool)

    def delete_rows(self, indexes):
        """
        Delete rows from the DataFrame

        :param indexes: either a list of values or list of booleans for the rows to delete
        :return: nothing
        """
        indexes = [indexes] if not isinstance(indexes, (list, blist)) else indexes
        if all([isinstance(i, bool) for i in indexes]): # boolean list
            if len(indexes) != len(self._index):
                raise ValueError('boolean indexes list must be same size of existing indexes')
            indexes = [i for i, x in enumerate(indexes) if x]
        else:
            indexes = [sorted_index(self._index, x) for x in indexes] if self._sorted \
                else [self._index.index(x) for x in indexes]
        indexes = sorted(indexes, reverse=True)  # need to sort and reverse list so deleting works
        for c, column in enumerate(self._columns):
            for i in indexes:
                del self._data[c][i]
        # now remove from index
        for i in indexes:
            del self._index[i]

    def delete_columns(self, columns):
        """
        Delete columns from the DataFrame

        :param columns: list of columns to delete
        :return: nothing
        """
        columns = [columns] if not isinstance(columns, (list, blist)) else columns
        if not all([x in self._columns for x in columns]):
            raise ValueError('all columns must be in current columns')
        for column in columns:
            c = self._columns.index(column)
            del self._data[c]
            del self._columns[c]
        if not len(self._data):  # if all the columns have been deleted, remove index
            self.index = list()

    @staticmethod
    def _sorted_list_indexes(list_to_sort, key=None, reverse=False):
        """
        Sorts a list but returns the order of the index values of the list for the sort and not the values themselves.
        For example is the list provided is ['b', 'a', 'c'] then the result will be [2, 1, 3]

        :param list_to_sort: list to sort
        :param key: if not None then a function of one argument that is used to extract a comparison key from each
                    list element
        :param reverse: if True then the list elements are sorted as if each comparison were reversed.
        :return: list of sorted index values
        """
        if key is not None:
            def key_func(i): return key(list_to_sort.__getitem__(i))
        else:
            key_func = list_to_sort.__getitem__
        return sorted(range(len(list_to_sort)), key=key_func, reverse=reverse)

    def sort_index(self):
        """
        Sort the DataFrame by the index. The sort modifies the DataFrame inplace

        :return: nothing
        """
        sort = self._sorted_list_indexes(self._index)
        # sort index
        self._index = blist([self._index[x] for x in sort]) if self._blist else [self._index[x] for x in sort]
        # each column
        for c in range(len(self._data)):
            self._data[c] = blist([self._data[c][i] for i in sort]) if self._blist else [self._data[c][i] for i in sort]

    def sort_columns(self, column, key=None, reverse=False):
        """
        Sort the DataFrame by one of the columns. The sort modifies the DataFrame inplace. The key and reverse
        parameters have the same meaning as for the built-in sorted() function.

        :param column: column name to use for the sort
        :param key: if not None then a function of one argument that is used to extract a comparison key from each
                    list element
        :param reverse: if True then the list elements are sorted as if each comparison were reversed.
        :return: nothing
        """
        if isinstance(column, (list, blist)):
            raise TypeError('Can only sort by a single column  ')
        sort = self._sorted_list_indexes(self._data[self._columns.index(column)], key, reverse)
        # sort index
        self._index = blist([self._index[x] for x in sort]) if self._blist else [self._index[x] for x in sort]
        # each column
        for c in range(len(self._data)):
            self._data[c] = blist([self._data[c][i] for i in sort]) if self._blist else [self._data[c][i] for i in sort]

    def _validate_index(self, indexes):
        if len(indexes) != len(set(indexes)):
            raise ValueError('index contains duplicates')
        if self._data:
            if len(indexes) != len(self._data[0]):
                raise ValueError('index length does not match data length')

    def _validate_columns(self, columns):
        if len(columns) != len(set(columns)):
            raise ValueError('columns contains duplicates')
        if self._data:
            if len(columns) != len(self._data):
                raise ValueError('number of column names does not match number of data columns')

    def _validate_data(self):
        if self._data:
            max_rows = max([len(x) for x in self._data])
            same_lens = all([len(x) == max_rows for x in self._data])
            if not same_lens:
                raise ValueError('data is corrupted, each column not all same length')

    def validate_integrity(self):
        """
        Validate the integrity of the DataFrame. This checks that the indexes, column names and internal data are not
        corrupted. Will raise an error if there is a problem.

        :return: nothing
        """
        self._validate_columns(self._columns)
        self._validate_index(self._index)
        self._validate_data()

    def append(self, data_frame):
        """
        Append another DataFrame to this DataFrame. If the new data_frame has columns that are not in the current
        DataFrame then new columns will be created. All of the indexes in the data_frame must be different from the
        current indexes or will raise an error.

        :param data_frame: DataFrame to append
        :return: nothing
        """
        data_frame_index = data_frame.index
        combined_index = self._index + data_frame_index
        if len(set(combined_index)) != len(combined_index):
            raise ValueError('duplicate indexes in DataFrames')

        for c, column in enumerate(data_frame.columns):
            if PYTHON3:
                self.set(indexes=data_frame_index, columns=column, values=data_frame.data[c].copy())
            else:
                self.set(indexes=data_frame_index, columns=column, values=data_frame.data[c][:])

    def equality(self, column, indexes=None, value=None):
        """
        Math helper method. Given a column and optional indexes will return a list of booleans on the equality of the
        value for that index in the DataFrame to the value parameter.

        :param column: column name to compare
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :param value: value to compare
        :return: list of booleans
        """
        indexes = [True] * len(self._index) if indexes is None else indexes
        compare_list = self.get_rows(indexes, column, as_list=True)
        return [x == value for x in compare_list]

    def _get_lists(self, left_column, right_column, indexes):
        indexes = [True] * len(self._index) if indexes is None else indexes
        left_list = self.get_rows(indexes, left_column, as_list=True)
        right_list = self.get_rows(indexes, right_column, as_list=True)
        return left_list, right_list

    def add(self, left_column, right_column, indexes=None):
        """
        Math helper method that adds element-wise two columns. If indexes are not None then will only perform the math
        on that sub-set of the columns.

        :param left_column: first column name
        :param right_column: second column name
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l + r for l, r in zip(left_list, right_list)]

    def subtract(self, left_column, right_column, indexes=None):
        """
        Math helper method that subtracts element-wise two columns. If indexes are not None then will only perform the
        math on that sub-set of the columns.

        :param left_column: first column name
        :param right_column: name of column to subtract from the left_column
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l - r for l, r in zip(left_list, right_list)]

    def multiply(self, left_column, right_column, indexes=None):
        """
        Math helper method that multiplies element-wise two columns. If indexes are not None then will only perform the
        math on that sub-set of the columns.

        :param left_column: first column name
        :param right_column: second column name
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l * r for l, r in zip(left_list, right_list)]

    def divide(self, left_column, right_column, indexes=None):
        """
        Math helper method that divides element-wise two columns. If indexes are not None then will only perform the
        math on that sub-set of the columns.

        :param left_column: column name of dividend
        :param right_column: column name of divisor
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l / r for l, r in zip(left_list, right_list)]

    def isin(self, column, compare_list):
        """
        Returns a boolean list where each elements is whether that element in the column is in the compare_list.

        :param column: single column name, does not work for multiple columns
        :param compare_list: list of items to compare to
        :return: list of booleans
        """
        return [x in compare_list for x in self._data[self._columns.index(column)]]

    def iterrows(self, index=True):
        """
        Iterates over DataFrame rows as dictionary of the values. The index will be included.

        :param index: if True include the index in the results
        :return: dictionary
        """
        for i in range(len(self._index)):
            row = {self._index_name: self._index[i]} if index else dict()
            for c, col in enumerate(self._columns):
                row[col] = self._data[c][i]
            yield row

    def itertuples(self, index=True, name='Raccoon'):
        """
        Iterates over DataFrame rows as tuple of the values.

        :param index: if True then include the index
        :param name: name of the namedtuple
        :return: namedtuple
        """
        fields = [self._index_name] if index else list()
        fields.extend(self._columns)
        row_tuple = namedtuple(name, fields)
        for i in range(len(self._index)):
            row = {self._index_name: self._index[i]} if index else dict()
            for c, col in enumerate(self._columns):
                row[col] = self._data[c][i]
            yield row_tuple(**row)

    def reset_index(self, drop=False):
        """
        Resets the index of the DataFrame to simple integer list and the index name to 'index'. If drop is True then
        the existing index is dropped, if drop is False then the current index is made a column in the DataFrame with
        the index name the name of the column. If the index is a tuple multi-index then each element of the tuple is
        converted into a separate column. If the index name was 'index' then the column name will be 'index_0' to not
        conflict on print().

        :param drop: if True then the current index is dropped, if False then index converted to columns
        :return: nothing
        """
        if not drop:
            if isinstance(self.index_name, tuple):
                index_data = list(map(list, zip(*self._index)))
                for i in range(len(self.index_name)):
                    self.set_column(column=self.index_name[i], values=index_data[i])
            else:
                col_name = self.index_name if self.index_name is not 'index' else 'index_0'
                self.set_column(column=col_name, values=self._index)
        self.index = list(range(self.__len__()))
        self.index_name = 'index'

    # DataFrame creation functions
    @classmethod
    def from_json(cls, json_string):
        """
        Creates and return a DataFrame from a JSON of the type created by to_json

        :param json_string: JSON
        :return: DataFrame
        """
        input_dict = json.loads(json_string)
        # convert index to tuple if required
        if input_dict['index'] and isinstance(input_dict['index'][0], list):
            input_dict['index'] = [tuple(x) for x in input_dict['index']]
        # convert index_name to tuple if required
        if isinstance(input_dict['meta_data']['index_name'], list):
            input_dict['meta_data']['index_name'] = tuple(input_dict['meta_data']['index_name'])
        data = input_dict['data'] if input_dict['data'] else None
        return cls(data=data, index=input_dict['index'], **input_dict['meta_data'])

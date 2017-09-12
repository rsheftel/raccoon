"""
Series class
"""
from __future__ import print_function
import six

import sys
from bisect import bisect_left, bisect_right
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from itertools import compress
from tabulate import tabulate
from blist import blist
from raccoon.sort_utils import sorted_exists, sorted_index, sorted_list_indexes

PYTHON3 = (sys.version_info >= (3, 0))


class SeriesBase(six.with_metaclass(ABCMeta)):
    """
    Base Series abstract base class that concrete implementations inherit from. Note that the .data and .index property
    methods in Series are views to the underlying data and not copies.
    """
    # Define slots to make object faster
    __slots__ = ['_data', '_data_name', '_index', '_index_name', '_sort']

    def __init__(self):
        """
        No specific parameters, those are defined in the child classed
        """
        self._index = None
        self._index_name = None
        self._data = None
        self._data_name = None
        self._sort = None

    def __len__(self):
        return len(self._index)

    def __repr__(self):
        return 'object id: %s\ndata:\n%s\nindex:\n%s\n' % (id(self), self._data, self._index)

    def __str__(self):
        return self._make_table()

    def _make_table(self, index=True, **kwargs):
        kwargs['headers'] = 'keys' if 'headers' not in kwargs.keys() else kwargs['headers']
        return tabulate(self.to_dict(ordered=True, index=index), **kwargs)

    def show(self, index=True, **kwargs):
        """
        Print the contents of the Series. This method uses the tabulate function from the tabulate package. Use the
        kwargs to pass along any arguments to the tabulate function.

        :param index: If True then include the indexes as a column in the output, if False ignore the index
        :param kwargs: Parameters to pass along to the tabulate function
        :return: output of the tabulate function
        """
        print(self._make_table(index=index, **kwargs))

    @property
    @abstractmethod
    def data(self):
        return

    @property
    @abstractmethod
    def index(self):
        return

    @index.setter
    @abstractmethod
    def index(self, index_list):
        return

    @property
    def data_name(self):
        return self._data_name

    @data_name.setter
    def data_name(self, name):
        self._data_name = name

    @property
    def index_name(self):
        return self._index_name

    @index_name.setter
    def index_name(self, name):
        self._index_name = name

    @property
    @abstractmethod
    def sort(self):
        return

    def get(self, indexes, as_list=False):
        """
        Given indexes will return a sub-set of the Series. This method will direct to the specific methods
        based on what types are passed in for the indexes. The type of the return is determined by the
        types of the parameters.

        :param indexes: index value, list of index values, or a list of booleans.
        :param as_list: if True then return the values as a list, if False return a Series.
        :return: either Series, list, or single value. The return is a shallow copy
        """
        if isinstance(indexes, (list, blist)):
            return self.get_rows(indexes, as_list)
        else:
            return self.get_cell(indexes)

    def get_cell(self, index):
        """
        For a single index and return the value

        :param index: index value
        :return: value
        """
        i = sorted_index(self._index, index) if self._sort else self._index.index(index)
        return self._data[i]

    def get_rows(self, indexes, as_list=False):
        """
        For a list of indexes return the values of the indexes in that column.

        :param indexes: either a list of index values or a list of booleans with same length as all indexes
        :param as_list: if True return a list, if False return Series
        :return: Series if as_list if False, a list if as_list is True
        """
        if all([isinstance(i, bool) for i in indexes]):  # boolean list
            if len(indexes) != len(self._index):
                raise ValueError('boolean index list must be same size of existing index')
            if all(indexes):  # the entire column
                data = self._data
                index = self._index
            else:
                data = list(compress(self._data, indexes))
                index = list(compress(self._index, indexes))
        else:  # index values list
            locations = [sorted_index(self._index, x) for x in indexes] if self._sort \
                else [self._index.index(x) for x in indexes]
            data = [self._data[i] for i in locations]
            index = [self._index[i] for i in locations]
        return data if as_list else Series(data=data, index=index, data_name=self._data_name,
                                           index_name=self._index_name, sort=self._sort)

    def get_location(self, location):
        """
        For an index location return a dict of the index and value. This is optimized for speed because
        it does not need to lookup the index location with a search. Also can accept relative indexing from the end of
        the SEries in standard python notation [-3, -2, -1]

        :param location: index location in standard python form of positive or negative number
        :return: dictionary
        """
        return {self.index_name: self._index[location], self.data_name: self._data[location]}

    def get_locations(self, locations, as_list=False):
        """
        For list of locations return a Series or list of the values.

        :param locations: list of index locations
        :param as_list: True to return a list of values
        :return: Series or list
        """

        indexes = [self._index[x] for x in locations]
        return self.get(indexes, as_list)

    def get_slice(self, start_index=None, stop_index=None, as_list=False):
        """
        For sorted Series will return either a Series or list of all of the rows where the index is greater than
        or equal to the start_index if provided and less than or equal to the stop_index if provided. If either the
        start or stop index is None then will include from the first or last element, similar to standard python
        slide of [:5] or [:5]. Both end points are considered inclusive.

        :param start_index: lowest index value to include, or None to start from the first row
        :param stop_index: highest index value to include, or None to end at the last row
        :param as_list: if True then return a list of the indexes and values
        :return: Series or tuple of (index list, values list)
        """
        if not self._sort:
            raise RuntimeError('Can only use get_slice on sorted Series')

        start_location = bisect_left(self._index, start_index) if start_index is not None else None
        stop_location = bisect_right(self._index, stop_index) if stop_index is not None else None

        index = self._index[start_location:stop_location]
        data = self._data[start_location:stop_location]

        if as_list:
            return index, data
        else:
            return Series(data=data, index=index, data_name=self._data_name, index_name=self._index_name,
                          sort=self._sort)

    def _slice_index(self, slicer):
        try:
            start_index = sorted_index(self._index, slicer.start) if self._sort else self._index.index(slicer.start)
        except ValueError:
            raise IndexError('start of slice not in the index')
        try:
            end_index = sorted_index(self._index, slicer.stop) if self._sort else self._index.index(slicer.stop)
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

    def _validate_index(self, indexes):
        if not(isinstance(indexes, (list, blist)) or indexes is None):
            raise TypeError('indexes must be list, blist or None')
        if len(indexes) != len(set(indexes)):
            raise ValueError('index contains duplicates')
        if self._data:
            if len(indexes) != len(self._data):
                raise ValueError('index length does not match data length')

    def validate_integrity(self):
        """
        Validate the integrity of the Series. This checks that the indexes, column names and internal data are not
        corrupted. Will raise an error if there is a problem.

        :return: nothing
        """
        self._validate_index(self._index)

    def to_dict(self, index=True, ordered=False):
        """
        Returns a dict where the keys are the data and index names and the values are list of the data and index.

        :param index: If True then include the index in the dict with the index_name as the key
        :param ordered: If True then return an OrderedDict() to preserve the order of the columns in the Series
        :return: dict or OrderedDict()
        """
        result = OrderedDict() if ordered else dict()
        if index:
            result.update({self._index_name: self._index})
        if ordered:
            data_dict = [(self._data_name, self._data)]
        else:
            data_dict = {self._data_name: self._data}
        result.update(data_dict)
        return result

    def head(self, rows):
        """
        Return a Series of the first N rows

        :param rows: number of rows
        :return: Series
        """
        rows_bool = [True] * min(rows, len(self._index))
        rows_bool.extend([False] * max(0, len(self._index) - rows))
        return self.get(indexes=rows_bool)

    def tail(self, rows):
        """
        Return a Series of the last N rows

        :param rows: number of rows
        :return: Series
        """
        rows_bool = [False] * max(0, len(self._index) - rows)
        rows_bool.extend([True] * min(rows, len(self._index)))
        return self.get(indexes=rows_bool)

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
            if self._sort:
                booleans[sorted_index(self._index, compare)] = True
            else:
                booleans[self._index.index(compare)] = True
        if result == 'boolean':
            return booleans
        elif result == 'value':
            return list(compress(self._index, booleans))
        else:
            raise ValueError('only valid values for result parameter are: boolean or value.')

    def isin(self, compare_list):
        """
        Returns a boolean list where each elements is whether that element in the column is in the compare_list.

        :param compare_list: list of items to compare to
        :return: list of booleans
        """
        return [x in compare_list for x in self._data]

    def equality(self, indexes=None, value=None):
        """
        Math helper method. Given a column and optional indexes will return a list of booleans on the equality of the
        value for that index in the DataFrame to the value parameter.

        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :param value: value to compare
        :return: list of booleans
        """
        indexes = [True] * len(self._index) if indexes is None else indexes
        compare_list = self.get_rows(indexes, as_list=True)
        return [x == value for x in compare_list]


class Series(SeriesBase):
    """
    Series class. The raccoon Series implements a simplified version of the pandas Series with the key
    objective difference that the raccoon Series is meant for use cases where the size of the Series is
    expanding frequently. This is known to be slow with Pandas due to the use of numpy as the underlying data structure.
    The Series can be designated as sort, in which case the rows will be sort by index on construction, 
    and then any addition of a new row will insert it into the Series so that the index remains sort.
    """
    def __init__(self, data=None, index=None, data_name='value', index_name='index', use_blist=False, sort=None):
        """
        :param data: (optional) list of values.
        :param index: (optional) list of index values. If None then the index will be integers starting with zero
        :param data_name: (optional) name of the data column, or will default to 'value'
        :param index_name: (optional) name for the index. Default is "index"
        :param use_blist: if True then use blist() as the underlying data structure, if False use standard list()
        :param sort: if True then Series will keep the index sort. If True all index values must be of same type
        """
        super(SeriesBase, self).__init__()

        # standard variable setup
        self._index = None
        self._index_name = index_name
        self._data = None
        self._data_name = data_name
        self._blist = use_blist

        # setup data list
        if data is None:
            self._data = blist() if self._blist else list()
            if index:
                # pad out to the number of rows
                self._pad_data(len(index))
                self.index = index
            else:
                self.index = list()
        elif isinstance(data, (list, blist)):
            self._data = blist([x for x in data]) if self._blist else [x for x in data]
            # setup index
            if index:
                self.index = index
            else:
                self.index = list(range(len(self._data)))
        else:
            raise TypeError('Not valid data type.')

        # setup sort
        self._sort = None
        if sort is not None:
            self.sort = sort
        else:
            if index:
                self.sort = False
            else:
                self.sort = True

    def _pad_data(self, index_len):
        """
        Pad the data in Series with [None] to ensure that data is the same length as index

        :param index_len: length of index to extend data to
        :return: nothing
        """
        self._data.extend([None] * (index_len - len(self._data)))

    @property
    def data(self):
        return self._data

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index_list):
        self._validate_index(index_list)
        self._index = blist(index_list) if self._blist else list(index_list)

    @property
    def blist(self):
        return self._blist

    @property
    def sort(self):
        return self._sort

    @sort.setter
    def sort(self, boolean):
        self._sort = boolean
        if self._sort:
            self.sort_index()

    def sort_index(self):
        """
        Sort the Series by the index. The sort modifies the Series inplace

        :return: nothing
        """
        sort = sorted_list_indexes(self._index)
        # sort index
        self._index = blist([self._index[x] for x in sort]) if self._blist else [self._index[x] for x in sort]
        # sort data
        self._data = blist([self._data[x] for x in sort]) if self._blist else [self._data[x] for x in sort]

    def set(self, indexes, values=None):
        """
        Given indexes will set a sub-set of the Series to the values provided. This method will direct to the below 
        methods based on what types are passed in for the indexes. If the indexes contains values not in the Series 
        then new rows or columns will be added.

        :param indexes: indexes value, list of indexes values, or a list of booleans.
        :param values: value or list of values to set. If a list then must be the same length as the indexes parameter.
        :return: nothing
        """
        if isinstance(indexes, (list, blist)):
            self.set_rows(indexes, values)
        else:
            self.set_cell(indexes, values)

    def _add_row(self, index):
        """
        Add a new row to the Series

        :param index: index of the new row
        :return: nothing
        """
        self._index.append(index)
        self._data.append(None)

    def _insert_row(self, i, index):
        """
        Insert a new row in the Series.

        :param i: index location to insert
        :param index: index value to insert into the index list
        :return: nothing
        """
        if i == len(self._index):
            self._add_row(index)
        else:
            self._index.insert(i, index)
            self._data.insert(i, None)

    def _add_missing_rows(self, indexes):
        """
        Given a list of indexes, find all the indexes that are not currently in the Series and make a new row for
        that index by appending to the Series. This does not maintain sorted order for the index.

        :param indexes: list of indexes
        :return: nothing
        """
        new_indexes = [x for x in indexes if x not in self._index]
        for x in new_indexes:
            self._add_row(x)

    def _insert_missing_rows(self, indexes):
        """
        Given a list of indexes, find all the indexes that are not currently in the Series and make a new row for
        that index, inserting into the index. This requires the Series to be sorted=True

        :param indexes: list of indexes
        :return: nothing
        """
        new_indexes = [x for x in indexes if x not in self._index]
        for x in new_indexes:
            self._insert_row(bisect_left(self._index, x), x)

    def set_cell(self, index, value):
        """
        Sets the value of a single cell. If the index is not in the current index then a new index will be created.

        :param index: index value
        :param value: value to set
        :return: nothing
        """
        if self._sort:
            exists, i = sorted_exists(self._index, index)
            if not exists:
                self._insert_row(i, index)
        else:
            try:
                i = self._index.index(index)
            except ValueError:
                i = len(self._index)
                self._add_row(index)
        self._data[i] = value

    def set_rows(self, index, values=None):
        """
        Set rows to a single value or list of values. If any of the index values are not in the current indexes
        then a new row will be created.

        :param index: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the Series
        :param values: either a single value or a list. The list must be the same length as the index list if the index\
        list is values, or the length of the True values in the index list if the index list is booleans
        :return: nothing
        """
        if all([isinstance(i, bool) for i in index]):  # boolean list
            if not isinstance(values, (list, blist)):  # single value provided, not a list, so turn values into list
                values = [values for x in index if x]
            if len(index) != len(self._index):
                raise ValueError('boolean index list must be same size of existing index')
            if len(values) != index.count(True):
                raise ValueError('length of values list must equal number of True entries in index list')
            indexes = [i for i, x in enumerate(index) if x]
            for x, i in enumerate(indexes):
                self._data[i] = values[x]
        else:  # list of index
            if not isinstance(values, (list, blist)):  # single value provided, not a list, so turn values into list
                values = [values for _ in index]
            if len(values) != len(index):
                raise ValueError('length of values and index must be the same.')
            # insert or append indexes as needed
            if self._sort:
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
                self._data[i] = values[x]

    def set_location(self, location, value):
        """
        For a location set the value
        
        :param location: location 
        :param value: value
        :return: nothing
        """
        self._data[location] = value

    def set_locations(self, locations, values):
        """
        For a list of locations set the values.

        :param locations: list of index locations
        :param values: list of values or a single value
        :return: nothing
        """

        indexes = [self._index[x] for x in locations]
        self.set(indexes, values)

    def __setitem__(self, index, value):
        """
        Convenience wrapper around the set() method for using srs[] = X
        Usage...

        df[1] -- set cell at index=1
        df[[0, 3]] -- set index=[0, 3]
        df[1:2] -- set index slice 1:2

        :param index: any of the parameter examples above
        :param value: single value or list of values
        :return: nothing
        """
        indexes = self._slice_index(index) if isinstance(index, slice) else index
        return self.set(indexes=indexes, values=value)

    def __getitem__(self, index):
        """
        Convenience wrapper around the get() method for using srs[]
        Usage...
        df[5, 'b']  -- get cell at index=5
        df[[4, 5], 'c'] -- get indexes=[4, 5]
        df[4:10]  -- get indexes=[4, 5, 6, 7, 8, 9, 10]
        can also use a boolean list for anything

        :param index: any of the parameters above
        :return: Series of the subset slice
        """
        if isinstance(index, slice):  # just a slice of index
            if self._sort:  # faster version for sort=True
                return self.get_slice(index.start, index.stop, as_list=False)
            else:
                return self.get(indexes=self._slice_index(index))
        else:  # just a single cell or list of cells
            return self.get(index)

    def append_row(self, index, value):
        """
        Appends a row of value to the end of the data. Be very careful with this function as for sorted Series it will 
        not enforce sort order. Use this only for speed when needed, be careful.

        :param index: index
        :param value: value
        :return: nothing
        """
        if index in self._index:
            raise IndexError('index already in Series')

        self._index.append(index)
        self._data.append(value)

    def append_rows(self, indexes, values):
        """
        Appends values to the end of the data. Be very careful with this function as for sort DataFrames it will not 
        enforce sort order. Use this only for speed when needed, be careful.

        :param indexes: list of indexes to append
        :param values: list of values to append
        :return: nothing
        """

        # check that the values data is less than or equal to the length of the indexes
        if len(values) != len(indexes):
            raise ValueError('length of values is not equal to length of indexes')

        # check the indexes are not duplicates
        combined_index = self._index + indexes
        if len(set(combined_index)) != len(combined_index):
            raise IndexError('duplicate indexes in Series')

        # append index value
        self._index.extend(indexes)
        self._data.extend(values)

    def delete(self, indexes):
        """
        Delete rows from the DataFrame

        :param indexes: either a list of values or list of booleans for the rows to delete
        :return: nothing
        """
        indexes = [indexes] if not isinstance(indexes, (list, blist)) else indexes
        if all([isinstance(i, bool) for i in indexes]):  # boolean list
            if len(indexes) != len(self._index):
                raise ValueError('boolean indexes list must be same size of existing indexes')
            indexes = [i for i, x in enumerate(indexes) if x]
        else:
            indexes = [sorted_index(self._index, x) for x in indexes] if self._sort \
                else [self._index.index(x) for x in indexes]
        indexes = sorted(indexes, reverse=True)  # need to sort and reverse list so deleting works
        for i in indexes:
            del self._data[i]
        # now remove from index
        for i in indexes:
            del self._index[i]

    def reset_index(self):
        """
        Resets the index of the Series to simple integer list and the index name to 'index'.

        :return: nothing
        """
        self.index = list(range(self.__len__()))
        self.index_name = 'index'


class ViewSeries(SeriesBase):
    """
    ViewSeries class. The raccoon ViewSeries implements a view only version of the Series object with the key
    objective difference that the raccoon ViewSeries is meant for view only use cases where the underlying index and
    data are modified elsewhere or static. Use this for a view into a single column of a DataFrame.
    """
    def __init__(self, data=None, index=None, data_name='value', index_name='index', sort=False, offset=0):
        """
        :param data: (optional) list of values.
        :param index: (optional) list of index values. If None then the index will be integers starting with zero
        :param data_name: (optional) name of the data column, or will default to 'value'
        :param index_name: (optional) name for the index. Default is "index"
        :param sort: if True then assumes the index is sorted for faster set/get operations
        :param offset: integer to add to location to transform to standard python list location index
        """
        super(SeriesBase, self).__init__()

        # check inputs
        if index is None:
            raise ValueError('Index cannot be None.')
        if data is None:
            raise ValueError('Data cannot be None.')
        if not isinstance(data, (list, blist)):
            raise TypeError('Not valid data type.')

        # standard variable setup
        self._data = data  # direct view, no copy
        self._data_name = data_name
        self.index = index  # direct view, no copy
        self._index_name = index_name
        self._sort = sort
        self._offset = offset

    @property
    def data(self):
        return self._data

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, index_list):
        self._validate_index(index_list)
        self._index = index_list

    @property
    def sort(self):
        return self._sort

    @property
    def offset(self):
        return self._offset

    def value(self, indexes, int_as_index=False):
        """
        Wrapper function for get. It will return a list, no index. If the indexes are integers it will be assumed
        that they are locations unless int_as_index = True. If the indexes are locations then they will be rotated to 
        the left by offset number of locations.

        :param indexes: integer location, single index, list of indexes or list of boolean
        :param int_as_index: if True then will treat int index values as indexes and not locations
        :return: value or list of values
        """
        # single integer value
        if isinstance(indexes, int):
            if int_as_index:
                return self.get(indexes, as_list=True)
            else:
                indexes = indexes - self._offset
                return self._data[indexes]

        # slice
        elif isinstance(indexes, slice):
            if isinstance(indexes.start, int) and not int_as_index:  # treat as location
                start = indexes.start - self._offset
                stop = indexes.stop - self._offset + 1  # to capture the last value
                # check locations are valid and will not return empty
                if start > stop:
                    raise IndexError('end of slice is before start of slice')
                if (start > 0 > stop) or (start < 0 < stop):
                    raise IndexError('slide indexes invalid with given offset:%f' % self._offset)
                # where end is the last element
                if (start < 0) and stop == 0:
                    return self._data[start:]
                return self._data[start:stop]
            else:  # treat as index
                indexes = self._slice_index(indexes)
                return self.get(indexes, as_list=True)

        # list of booleans
        elif all([isinstance(x, bool) for x in indexes]):
            return self.get(indexes, as_list=True)

        # list of values
        elif isinstance(indexes, list):
            if int_as_index or not isinstance(indexes[0], int):
                return self.get(indexes, as_list=True)
            else:
                indexes = [x - self._offset for x in indexes]
                return self.get_locations(indexes, as_list=True)

        # just a single value
        else:
            return self.get(indexes)

    def __getitem__(self, index):
        """
        Convenience wrapper around the value() method for using srs[]. This will treat all integers as locations

        Usage...
        df[5]  -- get cell at location=5
        df[[4, 5]] -- get locations=[4, 5]
        df[[-1:0]]  -- get locations at slices
        can also use a boolean list for anything

        :param index: any of the parameters above
        :return: DataFrame of the subset slice
        """
        return self.value(index, int_as_index=False)

    # Series creation functions
    @classmethod
    def from_dataframe(cls, dataframe, column, offset=0):
        """
        Creates and return a Series from a DataFrame and specific column

        :param dataframe: raccoon DataFrame
        :param column: column name
        :param offset: offset value must be provided as there is no equivalent for a DataFrame
        :return: Series
        """
        return cls(data=dataframe.get_entire_column(column, as_list=True), index=dataframe.index,
                   data_name=column, index_name=dataframe.index_name, sort=dataframe.sort, offset=offset)

    @classmethod
    def from_series(cls, series, offset=0):
        """
        Creates and return a Series from a Series

        :param series: raccoon Series
        :param offset: offset value must be provided as there is no equivalent for a DataFrame
        :return: Series
        """
        return cls(data=series.data, index=series.index, data_name=series.data_name, index_name=series.index_name,
                   sort=series.sort, offset=offset)

"""
Series class
"""
import sys
from collections import OrderedDict
from tabulate import tabulate
from blist import blist
from sort_utils import sorted_exists, sorted_index, sorted_list_indexes

PYTHON3 = (sys.version_info >= (3, 0))


class Series(object):
    """
    Series class. The raccoon Series implements a simplified version of the pandas Series with the key
    objective difference that the raccoon Series is meant for use cases where the size of the Series is
    expanding frequently. This is known to be slow with Pandas due to the use of numpy as the underlying data structure.
    The Series can be designated as sort, in which case the rows will be sort by index on construction, 
    and then any addition of a new row will insert it into the Series so that the index remains sort.
    """
    def __init__(self, data=None, data_name='value', index=None, index_name='index', use_blist=False, sort=None,
                 offset=0):
        """
        :param data: (optional) list of values.
        :param data_name: (optional) name of the data column, or will default to 'value'
        :param index: (optional) list of index values. If None then the index will be integers starting with zero
        :param index_name: (optional) name for the index. Default is "index"
        :param use_blist: if True then use blist() as the underlying data structure, if False use standard list()
        :param sort: if True then DataFrame will keep the index sort. If True all index values must be of same type
        :param offset: integer to add to location to transform to standard python list location index
        """

        # standard variable setup
        self._index = None
        self._index_name = index_name
        self._data = None
        self._data_name = data_name
        self._blist = use_blist
        self._offset = offset

        # setup data list
        if data is None:
            self._data = blist() if self._blist else list()
            if index:
                # pad out to the number of rows
                self._pad_data(max_len=len(index))
                self.index = index
            else:
                self.index = list()
        elif isinstance(data, list):
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

    def _pad_data(self, max_len=None):
        """
        Pad the data in Series with [None} to ensure that data is the same length as index

        :param max_len: If provided will extend data to this length, if not then will use the index length
        :return: nothing
        """
        if not max_len:
            max_len = len(self._index)
        self._data.extend([None] * (max_len - len(self._data)))

    @property
    def data(self):
        if PYTHON3:
            return self._data.copy()
        else:
            return self._data[:]

    @property
    def data_name(self):
        return self._data_name

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
    def sort(self):
        return self._sort

    @sort.setter
    def sort(self, boolean):
        self._sort = boolean
        if self._sort:
            self.sort_index()

    @property
    def offset(self):
        return self._offset

    def sort_index(self):
        """
        Sort the DataFrame by the index. The sort modifies the DataFrame inplace

        :return: nothing
        """
        sort = sorted_list_indexes(self._index)
        # sort index
        self._index = blist([self._index[x] for x in sort]) if self._blist else [self._index[x] for x in sort]
        # sort data
        self._data = blist([self._data[x] for x in sort]) if self._blist else [self._data[x] for x in sort]

    def _validate_index(self, indexes):
        if not(isinstance(indexes, list) or indexes is None):
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
        Returns a dict where the keys are the column name and the values are list of the values for that column.

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


class ViewSeries(Series):
    """
    ViewSeries class. The raccoon ViewSeries implements a view only version of the Series object with the key
    objective difference that the raccoon ViewSeries is meant for view only use cases where the underlying index and
    data are modified elsewhere or static. Use this for a view into a single column of a DataFrame.
    """
    def __init__(self, data=None, data_name='value', index=None, index_name='index', sort=False, offset=0):
        """
        :param data: (optional) list of values.
        :param data_name: (optional) name of the data column, or will default to 'value'
        :param index: (optional) list of index values. If None then the index will be integers starting with zero
        :param index_name: (optional) name for the index. Default is "index"
        :param sort: if True then DataFrame will keep the index sort. If True all index values must be of same type
        :param offset: integer to add to location to transform to standard python list location index
        """
        # check inputs
        if index is None:
            raise ValueError('Index cannot be None.')
        if data is None:
            raise ValueError('Data cannot be None.')
        if not isinstance(data, list):
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
    def blist(self):
        raise NotImplementedError

    @property
    def sort(self):
        return self._sort

    @sort.setter
    def sort(self, boolean):
        raise NotImplementedError

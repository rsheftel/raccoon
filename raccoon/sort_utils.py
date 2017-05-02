"""
Utility functions for sorting and dealing with sorted Series and DataFrames
"""

from bisect import bisect_left, bisect_right


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


def sorted_list_indexes(list_to_sort, key=None, reverse=False):
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
        def key_func(i):
            return key(list_to_sort.__getitem__(i))
    else:
        key_func = list_to_sort.__getitem__
    return sorted(range(len(list_to_sort)), key=key_func, reverse=reverse)

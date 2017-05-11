import pytest
import raccoon as rc
from collections import OrderedDict
from copy import deepcopy
from raccoon.utils import assert_series_equal
from blist import blist


def test_names():
    srs = rc.Series([1, 2])
    assert srs.index_name == 'index'
    assert srs.data_name == 'value'

    srs.index_name = 'new_index'
    srs.data_name = 'data'
    assert srs.index_name == 'new_index'
    assert srs.data_name == 'data'


def test_use_blist():
    def check_blist():
        assert isinstance(srs.index, blist)
        assert isinstance(srs.data, blist)

    srs = rc.Series(use_blist=True)
    assert isinstance(srs, rc.Series)
    assert srs.data == []
    assert srs.index == []
    assert srs.sort is True
    check_blist()

    # add a new row and col
    srs.set_cell(1, 1)
    check_blist()

    # add a new row
    srs.set_cell(2, 2)
    check_blist()

    # add a new col
    srs.set_cell(1, 3)
    check_blist()

    # add a complete new row
    srs.set_rows([3], [5])
    check_blist()


def test_default_list():
    def check_list():
        assert isinstance(srs.index, list)
        assert isinstance(srs.data, list)

    srs = rc.Series()
    assert isinstance(srs, rc.Series)
    assert srs.data == []
    assert srs.index == []
    assert srs.sort is True
    check_list()

    # add a new row and col
    srs.set_cell(1, 1)
    check_list()

    # add a new row
    srs.set_cell(2, 2)
    check_list()

    # add a complete new row
    srs.set_rows([3], [5])
    check_list()


def test_to_dict():
    srs = rc.Series([1, 2, 3], index=['a', 'b', 'c'], data_name='a')

    # with index
    actual = srs.to_dict(index=True)
    assert actual == {'index': ['a', 'b', 'c'], 'a': [1, 2, 3]}

    # without index
    actual = srs.to_dict(index=False)
    assert actual == {'a': [1, 2, 3]}

    # ordered
    act_order = srs.to_dict(ordered=True)
    expected = OrderedDict([('index', ['a', 'b', 'c']), ('a', [1, 2, 3])])
    assert act_order == expected


def test_show():
    srs = rc.Series([1.0, 2.55, 3.1], data_name='boo', index=['row1', 'row2', 'row3'], use_blist=True)

    # __repr__ produces a simple representation
    expected = "object id: %s\ndata:\nblist([1.0, 2.55, 3.1])\nindex:\nblist(['row1', 'row2', 'row3'])\n" % id(srs)
    actual = srs.__repr__()
    assert actual == expected

    # __str__ produces the standard table
    expected = 'index      boo\n-------  -----\nrow1      1\nrow2      2.55\nrow3      3.1'
    actual = srs.__str__()
    assert actual == expected

    # show() method will pass along any argument for the tabulate.tabulate function
    srs.show()


def test_input_data_mutability():
    input_data = [[1, 2, 3], [4, 5, 6]]

    # without defining column order
    srs = rc.Series(input_data)
    orig_data = deepcopy(srs.data)

    # change input_data
    input_data[1] = [6, 7, 8]
    assert srs.data != input_data
    assert srs.data == orig_data

    # change an inner index of input data
    input_data.append(99)
    assert srs.data == orig_data

    # Now make an inner element a mutable item, confirm that mutability remains
    input_data = [[1], [2], [3], [4, 5, 6]]

    srs = rc.Series(input_data)
    orig_data = deepcopy(srs.data)

    # changing the input data changes the inner data in Series
    input_data[0].append(11)
    assert srs.data != orig_data
    assert srs.get(0) == [1, 11]

    # changing the entire inner element
    srs[1] = [2, 22]
    assert input_data == [[1, 11], [2], [3], [4, 5, 6]]
    assert srs.data == [[1, 11], [2, 22], [3], [4, 5, 6]]


def test_get_data_mutability():
    # the .data method only returns a view, and changes to the return values will corrupt the Series
    srs = rc.Series([1.0, 2.55, 3.1])
    orig_data = deepcopy(srs.data)
    data = srs.data

    # regular Series return a view of data
    data.append(99)
    assert srs.data != orig_data
    assert srs.data == [1.0, 2.55, 3.1, 99]

    # using the get commands returns a shallow copy
    srs = rc.Series([[1], [2], [3]])

    # mutate inner value
    srs[1].append(22)
    # changes the new_df
    assert srs.data == [[1], [2, 22], [3]]


def test_len():
    srs = rc.Series([], [])
    assert len(srs) == 0

    srs = rc.Series([1.0, 2.55, 3.1], sort=False)
    assert len(srs) == 3


def test_equality():
    srs = rc.Series([1, 2, 1, 2, 1, 1])
    assert srs.sort is True

    assert srs.equality(value=1) == [True, False, True, False, True, True]
    assert srs.equality([1, 2, 3], 2) == [True, False, True]
    assert srs.equality([False, False, False, True, True, True], 1) == [False, True, True]

    # change all 1 to 3
    srs.set(indexes=srs.equality(value=1), values=3)
    assert srs.data == [3, 2, 3, 2, 3, 3]

    srs = rc.Series([1, 2, 1, 2, 1, 1], sort=False)
    assert srs.sort is False

    assert srs.equality(value=1) == [True, False, True, False, True, True]
    assert srs.equality([1, 2, 3], 2) == [True, False, True]
    assert srs.equality([False, False, False, True, True, True], 1) == [False, True, True]

    # not enough booleans to match index len
    with pytest.raises(ValueError):
        srs.equality([True, True], 2)


def test_select_index():
    # simple index, not sort
    srs = rc.Series([1, 2, 3, 4, 5, 6], index=['a', 'b', 'c', 'd', 'e', 'f'])

    actual = srs.select_index('c', 'value')
    assert actual == ['c']

    actual = srs.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]

    # simple index, sort
    srs = rc.Series([1, 2, 3, 4, 5, 6], index=['a', 'b', 'c', 'd', 'e', 'f'], sort=True)

    actual = srs.select_index('c', 'value')
    assert actual == ['c']

    actual = srs.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]

    with pytest.raises(ValueError):
        srs.select_index('a', 'BAD')

    # simple index, not sort, blist
    srs = rc.Series([1, 2, 3, 4, 5, 6], index=['a', 'b', 'c', 'd', 'e', 'f'], use_blist=True)

    actual = srs.select_index('c', 'value')
    assert actual == ['c']

    actual = srs.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]

    # tuple index
    tuples = [('a', 1, 3), ('a', 1, 4), ('a', 2, 3), ('b', 1, 4), ('b', 2, 1), ('b', 3, 3)]
    srs = rc.Series([1, 2, 3, 4, 5, 6], index=tuples)

    compare = ('a', None, None)
    assert srs.select_index(compare) == [True, True, True, False, False, False]

    compare = ('a', None, 3)
    assert srs.select_index(compare, 'boolean') == [True, False, True, False, False, False]

    compare = (None, 2, None)
    assert srs.select_index(compare, 'value') == [('a', 2, 3), ('b', 2, 1)]

    compare = (None, 3, 3)
    assert srs.select_index(compare) == [False, False, False, False, False, True]

    compare = (None, None, 3)
    assert srs.select_index(compare, 'value') == [('a', 1, 3), ('a', 2, 3), ('b', 3, 3)]

    compare = ('a', 1, 4)
    assert srs.select_index(compare, 'value') == [('a', 1, 4)]

    compare = ('a', 100, 99)
    assert srs.select_index(compare, 'value') == []

    compare = (None, None, None)
    assert srs.select_index(compare) == [True] * 6

    srs = rc.Series([1, 2, 3, 4, 5, 6])
    assert srs.select_index(3) == [False, False, False, True, False, False]
    assert srs.select_index(3, 'value') == [3]


def test_isin():
    srs = rc.Series([1, 2, 3, 4, 5])

    assert srs.isin([2, 3, 4]) == [False, True, True, True, False]
    assert srs.isin([3]) == [False, False, True, False, False]
    assert srs.isin([6, 7]) == [False, False, False, False, False]


def test_reset_index():
    # no index defined
    srs = rc.Series([4, 5, 6])
    srs.reset_index()
    expected = rc.Series([4, 5, 6])
    assert_series_equal(srs, expected)

    # with index and index name defined
    srs = rc.Series([1, 2, 3], index=['x', 'y', 'z'], index_name='jelo')
    srs.reset_index()
    expected = rc.Series([1, 2, 3], [0, 1, 2], sort=False)
    assert_series_equal(srs, expected)

import pytest
import raccoon as rc
from collections import OrderedDict
from copy import deepcopy
from raccoon.utils import assert_frame_equal
from blist import blist


def test_use_blist():
    def check_blist():
        assert isinstance(df.index, blist)
        assert isinstance(df.columns, blist)
        assert isinstance(df.data, blist)
        assert all([isinstance(df.data[x], blist) for x in range(len(df.columns))])

    df = rc.DataFrame(use_blist=True)
    assert isinstance(df, rc.DataFrame)
    assert df.data == []
    assert df.columns == []
    assert df.index == []
    assert df.sort is True
    check_blist()

    # add a new row and col
    df.set_cell(1, 'a', 1)
    check_blist()

    # add a new row
    df.set_cell(2, 'a', 2)
    check_blist()

    # add a new col
    df.set_cell(1, 'b', 3)
    check_blist()

    # add a complete new row
    df.set_row(3, {'a': 4, 'b': 5})
    check_blist()

    # add a complete new col
    df.set_column([2, 3], 'c', [6, 7])
    check_blist()


def test_default_list():
    def check_list():
        assert isinstance(df.index, list)
        assert isinstance(df.columns, list)
        assert isinstance(df.data, list)
        assert all([isinstance(df.data[x], list) for x in range(len(df.columns))])

    df = rc.DataFrame()
    assert isinstance(df, rc.DataFrame)
    assert df.data == []
    assert df.columns == []
    assert df.index == []
    assert df.sort is True
    check_list()

    # add a new row and col
    df.set_cell(1, 'a', 1)
    check_list()

    # add a new row
    df.set_cell(2, 'a', 2)
    check_list()

    # add a new col
    df.set_cell(1, 'b', 3)
    check_list()

    # add a complete new row
    df.set_row(3, {'a': 4, 'b': 5})
    check_list()

    # add a complete new col
    df.set_column([2, 3], 'c', [6, 7])
    check_list()


def test_to_dict():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])

    # with index
    actual = df.to_dict(index=True)
    assert actual == {'index': ['a', 'b', 'c'], 'a': [1, 2, 3], 'b': [4, 5, 6]}

    # without index
    actual = df.to_dict(index=False)
    assert actual == {'a': [1, 2, 3], 'b': [4, 5, 6]}

    # ordered
    act_order = df.to_dict(ordered=True)
    expected = OrderedDict([('index', ['a', 'b', 'c']), ('b', [4, 5, 6]), ('a', [1, 2, 3])])
    assert act_order == expected


def test_to_list():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[4, 5, 6], columns=['b', 'a', 'c'])

    assert df['b'].to_list() == [4, 5, 6]
    assert df[[4, 6], 'a'].to_list() == [1, 3]
    assert df[4:5, 'c'].to_list() == [7, 8]
    assert df[[6], 'c'].to_list() == [9]

    # cannot to_list on a multi-column DataFrame
    with pytest.raises(TypeError):
        df.to_list()


def test_json():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[4, 5, 6], columns=['b', 'a', 'c'])

    str = df.to_json()
    actual = rc.DataFrame.from_json(str)
    assert_frame_equal(df, actual)

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, use_blist=True, sort=False)

    str = df.to_json()
    actual = rc.DataFrame.from_json(str)
    assert_frame_equal(df, actual)

    # empty DataFrame
    df = rc.DataFrame({'a': [], 'b': [], 'c': []})
    str = df.to_json()
    actual = rc.DataFrame.from_json(str)
    assert_frame_equal(df, actual)

    df = rc.DataFrame()
    str = df.to_json()
    actual = rc.DataFrame.from_json(str)
    assert_frame_equal(df, actual)


def test_json_objects():
    # test with a compound object returning a representation
    df = rc.DataFrame({'a': [1, 2], 'b': [4, blist([5, 6])]})

    str = df.to_json()
    actual = rc.DataFrame.from_json(str)

    # the DataFrames are not equal because the blist() was converted to a representation
    with pytest.raises(AssertionError):
        assert_frame_equal(df, actual)

    assert actual[1, 'b'] != blist([5, 6])
    assert actual[1, 'b'] == 'blist([5, 6])'

def test_json_multi_index():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[('a', 4), ('b', 5), ('c', 6)])

    str = df.to_json()
    actual = rc.DataFrame.from_json(str)
    assert_frame_equal(df, actual)

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[('a', 4), ('b', 5), ('c', 6)],
                      index_name=('first', 'second'))

    str = df.to_json()
    actual = rc.DataFrame.from_json(str)
    assert_frame_equal(df, actual)


def test_append():
    # duplicate indexes
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[0, 1, 2])
    df2 = rc.DataFrame({'a': [11, 12, 13], 'b': [14, 15, 16]}, columns=['a', 'b'], index=[2, 3, 4])
    with pytest.raises(ValueError):
        df.append(df2)

    # all same columns
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[0, 1, 2])
    df2 = rc.DataFrame({'a': [11, 12, 13], 'b': [14, 15, 16]}, columns=['a', 'b'], index=[3, 4, 5])
    df.append(df2)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3, 11, 12, 13], 'b': [4, 5, 6, 14, 15, 16]},
                                        columns=['a', 'b'], index=[0, 1, 2, 3, 4, 5]))

    # all new columns
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[0, 1, 2])
    df2 = rc.DataFrame({'x': [11, 12, 13], 'y': [14, 15, 16]}, columns=['x', 'y'], index=[3, 4, 5])
    df.append(df2)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3, None, None, None], 'b': [4, 5, 6, None, None, None],
                                         'x': [None, None, None, 11, 12, 13], 'y': [None, None, None, 14, 15, 16]},
                                        columns=['a', 'b', 'x', 'y'], index=[0, 1, 2, 3, 4, 5]))

    # some same, some new columns
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[0, 1, 2])
    df2 = rc.DataFrame({'b': [11, 12, 13], 'y': [14, 15, 16]}, columns=['b', 'y'], index=[3, 4, 5])
    df.append(df2)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3, None, None, None], 'b': [4, 5, 6, 11, 12, 13],
                                         'y': [None, None, None, 14, 15, 16]},
                                        columns=['a', 'b', 'y'], index=[0, 1, 2, 3, 4, 5]))

    # append empty DataFrame
    df2 = rc.DataFrame(columns=['a', 'b', 'y'])
    df.append(df2)
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3, None, None, None], 'b': [4, 5, 6, 11, 12, 13],
                                         'y': [None, None, None, 14, 15, 16]},
                                        columns=['a', 'b', 'y'], index=[0, 1, 2, 3, 4, 5]))


def test_rename_columns():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])

    df.rename_columns({'b': 'b_new'})
    assert df.columns == ['b_new', 'a']

    df.rename_columns({'b_new': 'b2', 'a': 'a2'})
    assert df.columns == ['b2', 'a2']

    with pytest.raises(ValueError):
        df.rename_columns({'a2': 'a', 'bad': 'nogo'})


def test_show():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [1.0, 2.55, 3.1], 'c': ['first', 'second', None]}, columns=['b', 'c', 'a'],
                      index=['row1', 'row2', 'row3'], use_blist=True)

    # __repr__ produces a simple representation
    expected = "object id: %s\ncolumns:\nblist(['b', 'c', 'a'])\ndata:\nblist([blist([1.0, 2.55, 3.1]), blist([" \
               "'first', 'second', None]), blist([1, 2, 3])])\nindex:\nblist(['row1', 'row2', 'row3'])\n" % id(df)
    actual = df.__repr__()
    assert actual == expected

    # __str__ produces the standard table
    expected = 'index       b  c         a\n-------  ----  ------  ---\nrow1     1     first     1\n' \
               'row2     2.55  second    2\nrow3     3.1             3'
    actual = df.__str__()
    assert actual == expected

    # show() method will pass along any argument for the tabulate.tabulate function
    df.show()


def test_input_data_mutability():
    input_data = {'a': [1, 2, 3], 'b': [4, 5, 6]}

    # without defining column order
    df = rc.DataFrame(input_data)
    orig_data = deepcopy(df.data)

    # change input_data
    input_data['c'] = [6, 7, 8]
    assert df.to_dict(index=False) != input_data
    assert df.data == orig_data

    # change an inner index of input data
    input_data['a'].append(99)
    assert df.data == orig_data

    # Now make an inner element a mutable item, confirm that mutability remains
    input_data = {'a': [[1], [2], [3]], 'b': [4, 5, 6]}

    df = rc.DataFrame(input_data)
    orig_data = deepcopy(df.data)

    # changing the input data changes the inner data in DataFrame
    input_data['a'][0].append(11)
    assert df.data != orig_data
    assert df.get(0, 'a') == [1, 11]

    # using set to change the DataFrame data does not effect the input data
    df[1, 'a'] = [2, 22]
    assert input_data['a'] == [[1, 11], [2], [3]]

    df.set(columns='b', values=[44, 55, 66])
    assert input_data['b'] == [4, 5, 6]


def test_get_data_mutability():
    # the .data method only returns a shallow copy, and changes to the return values will corrupt the DataFrame
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [1.0, 2.55, 3.1], 'c': ['first', 'second', None]}, columns=['a', 'b', 'c'])
    orig_data = deepcopy(df.data)
    data = df.data

    data[0].append(99)
    assert df.data != orig_data
    assert df.data[0] == [1, 2, 3, 99]

    # using the get commands returns a shallow copy
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [[1], [2], [3]]}, columns=['a', 'b'])
    orig_data = deepcopy(df.data)

    new_df = df['a']
    new_df[3, 'a'] = 100
    assert df.data == orig_data

    # get a slice
    new_df = df['b']
    # mutate inner value
    new_df[1, 'b'].append(22)
    # changes the new_df
    assert new_df.data == [[[1], [2, 22], [3]]]
    # changes original df
    assert new_df.data[0] == df.data[1]


def test_len():
    df = rc.DataFrame()
    assert len(df) == 0

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [1.0, 2.55, 3.1]}, columns=['a', 'b'], sort=False)
    assert len(df) == 3

    df['a', 3] = 99
    assert len(df) == 4


def test_equality():
    df = rc.DataFrame({'z': [1, 2, 1, 2, 1, 1]})
    assert df.sort is True

    assert df.equality('z', value=1) == [True, False, True, False, True, True]
    assert df.equality('z', [1, 2, 3], 2) == [True, False, True]
    assert df.equality('z', [False, False, False, True, True, True], 1) == [False, True, True]

    # change all 1 to 3
    df.set(indexes=df.equality('z', value=1), columns='z', values=3)
    assert df.data == [[3, 2, 3, 2, 3, 3]]

    df = rc.DataFrame({'z': [1, 2, 1, 2, 1, 1]}, sort=False)
    assert df.sort is False

    assert df.equality('z', value=1) == [True, False, True, False, True, True]
    assert df.equality('z', [1, 2, 3], 2) == [True, False, True]
    assert df.equality('z', [False, False, False, True, True, True], 1) == [False, True, True]

    # not enough booleans to match index len
    with pytest.raises(ValueError):
        df.equality('z', [True, True], 2)


def test_math():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, columns=['a', 'b'])

    res = df.add('a', 'b')
    assert res == [6, 8, 10, 12]

    df['c'] = res
    assert df.data == [[1, 2, 3, 4], [5, 6, 7, 8], [6, 8, 10, 12]]
    assert df.columns == ['a', 'b', 'c']

    res = df.add('a', 'b', [1, 3])
    assert res == [8, 12]

    res = df.subtract('c', 'b')
    assert res == [1, 2, 3, 4]

    res = df.multiply('a', 'c', [True, True, False, False])
    assert res == [6, 16]

    res = df.divide('b', 'c', [0, 2])
    assert res == [5/6, 7/10]

    with pytest.raises(ValueError):
        df.multiply('a', 'c', [True, True])


def test_select_index():
    # simple index, not sort
    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]}, index=['a', 'b', 'c', 'd', 'e', 'f'])

    actual = df.select_index('c', 'value')
    assert actual == ['c']

    actual = df.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]

    # simple index, sort
    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]}, index=['a', 'b', 'c', 'd', 'e', 'f'], sort=True)

    actual = df.select_index('c', 'value')
    assert actual == ['c']

    actual = df.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]

    with pytest.raises(ValueError):
        df.select_index('a', 'BAD')

    # simple index, not sort, blist
    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]}, index=['a', 'b', 'c', 'd', 'e', 'f'], use_blist=True)

    actual = df.select_index('c', 'value')
    assert actual == ['c']

    actual = df.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]

    # tuple index
    tuples = [('a', 1, 3), ('a', 1, 4), ('a', 2, 3), ('b', 1, 4), ('b', 2, 1), ('b', 3, 3)]
    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]}, index=tuples)

    compare = ('a', None, None)
    assert df.select_index(compare) == [True, True, True, False, False, False]

    compare = ('a', None, 3)
    assert df.select_index(compare, 'boolean') == [True, False, True, False, False, False]

    compare = (None, 2, None)
    assert df.select_index(compare, 'value') == [('a', 2, 3), ('b', 2, 1)]

    compare = (None, 3, 3)
    assert df.select_index(compare) == [False, False, False, False, False, True]

    compare = (None, None, 3)
    assert df.select_index(compare, 'value') == [('a', 1, 3), ('a', 2, 3), ('b', 3, 3)]

    compare = ('a', 1, 4)
    assert df.select_index(compare, 'value') == [('a', 1, 4)]

    compare = ('a', 100, 99)
    assert df.select_index(compare, 'value') == []

    compare = (None, None, None)
    assert df.select_index(compare) == [True] * 6

    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]})
    assert df.select_index(3) == [False, False, False, True, False, False]
    assert df.select_index(3, 'value') == [3]


def test_isin():
    df = rc.DataFrame({'first': [1, 2, 3, 4, 5], 'second': ['a', 2, 'b', None, 5]})

    assert df.isin('first', [2, 3, 4]) == [False, True, True, True, False]
    assert df.isin('first', [3]) == [False, False, True, False, False]
    assert df.isin('first', [6, 7]) == [False, False, False, False, False]

    assert df.isin('second', ['a', 2]) == [True, True, False, False, False]
    assert df.isin('second', ['a', 'b']) == [True, False, True, False, False]
    assert df.isin('second', ['a', 'b', None]) == [True, False, True, True, False]


def test_reset_index():
    # no index defined
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'])
    df.reset_index()
    expected = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'index_0': [0, 1, 2]}, columns=['a', 'b', 'index_0'])
    assert_frame_equal(df, expected)

    # with index and index name defined
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=['x', 'y', 'z'], index_name='jelo')
    df.reset_index()
    expected = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'jelo': ['x', 'y', 'z']}, columns=['a', 'b', 'jelo'],
                            sort=False)
    assert_frame_equal(df, expected)

    # with a tuple multi-index
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'],
                      index=[('a', 10, 'x'), ('b', 11, 'y'), ('c', 12, 'z')], index_name=('melo', 'helo', 'gelo'))
    df.reset_index()
    expected = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'melo': ['a', 'b', 'c'], 'helo': [10, 11, 12],
                             'gelo': ['x', 'y', 'z']}, columns=['a', 'b', 'melo', 'helo', 'gelo'],
                            sort=False)
    assert_frame_equal(df, expected)

    # drop
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=['x', 'y', 'z'], index_name='jelo')
    df.reset_index(drop=True)
    expected = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], }, columns=['a', 'b'], sort=False)
    assert_frame_equal(df, expected)

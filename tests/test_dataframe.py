import pytest
import raccoon as rc
from raccoon.utils import assert_frame_equal
from collections import OrderedDict
from copy import deepcopy


def test_initialization():
    # solid matrix, no columns, no index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    assert set(tuple(x) for x in actual.data) == {(1, 2, 3), (4, 5, 6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == [0, 1, 2]

    # solid matrix, no columns, with index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], index_name='letters')
    assert set(tuple(x) for x in actual.data) == {(1, 2, 3), (4, 5, 6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == ['a', 'b', 'c']
    assert actual.index_name == 'letters'

    # solid matrix, columns, index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    assert actual.data == [[4, 5, 6], [1, 2, 3]]
    assert actual.columns == ['b', 'a']
    assert actual.index == ['a', 'b', 'c']

    # dict values are not lists
    actual = rc.DataFrame({'a': 1, 'b': 2, 'c': [1, 2, 3]}, columns=['b', 'c', 'a'])
    assert actual.columns == ['b', 'c', 'a']
    assert actual.index == [0, 1, 2]
    assert actual.data == [[2, None, None], [1, 2, 3], [1, None, None]]


def test_jagged_data():
    actual = rc.DataFrame({'a': [], 'b': [1], 'c': [1, 2], 'd': [1, 2, 3]}, columns=['a', 'b', 'c', 'd'])
    assert actual.data == [[None, None, None], [1, None, None], [1, 2, None], [1, 2, 3]]
    assert actual.columns == ['a', 'b', 'c', 'd']
    assert actual.index == [0, 1, 2]


def test_empty_initialization():
    actual = rc.DataFrame()
    assert isinstance(actual, rc.DataFrame)
    assert actual.data == []
    assert actual.columns == []
    assert actual.index == []

    actual = rc.DataFrame(columns=['a', 'b', 'c'])
    assert actual.data == [[], [], []]
    assert actual.columns == ['a', 'b', 'c']
    assert actual.index == []

    actual = rc.DataFrame(index=[1, 2, 3], columns=['a', 'b'])
    assert actual.data == [[None, None, None], [None, None, None]]
    assert actual.columns == ['a', 'b']
    assert actual.index == [1, 2, 3]


def test_bad_initialization():
    # index but no columns
    with pytest.raises(ValueError):
        rc.DataFrame(index=[1, 2, 3])

    # wrong number in index
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [1, 2, 3]}, index=[1])

    # wrong number of columns
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a'])

    with pytest.raises(ValueError):
        rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b', 'c', 'TOO', 'MANY'])

    # columns does not match dict keys
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['BAD', 'VALUE'])

    # index is not a list
    with pytest.raises(TypeError):
        rc.DataFrame({'a': [1]}, index=1)

    # columns is not a list
    with pytest.raises(TypeError):
        rc.DataFrame({'a': [1]}, columns='a')


def test_columns():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    names = actual.columns
    assert names == ['b', 'a']

    # test that a copy is returned
    names.append('bad')
    assert actual.columns == ['b', 'a']

    actual.columns = ['new1', 'new2']
    assert actual.columns == ['new1', 'new2']

    with pytest.raises(ValueError):
        actual.columns = ['list', 'too', 'long']


def test_index():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    result = actual.index
    assert result == ['a', 'b', 'c']

    # test that a copy is returned
    result.append('bad')
    assert actual.index == ['a', 'b', 'c']

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]

    assert actual.index_name == 'index'
    actual.index_name = 'new name'
    assert actual.index_name == 'new name'

    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], index_name='letters')
    assert actual.index_name == 'letters'


def test_data():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    assert actual.data == [[4, 5, 6], [1, 2, 3]]

    # test shallow copy
    new = actual.data
    new[0][0] = 99
    assert actual.data == new

    new.append(88)
    assert actual.data != new

    with pytest.raises(AttributeError):
        actual.data = [4, 5]


def test_set_cell():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    # change existing value
    actual.set(11, 'b', 55)
    assert actual.get(11, 'b') == 55
    actual.set(10, 'a', 11)
    assert actual.get(10, 'a') == 11
    actual.set(10, 'c', 13)
    assert actual.get(10, 'c') == 13
    assert actual.data == [[11, 2, 3], [4, 55, 6], [13, 8, 9]]

    # add a new row
    actual.set(13, 'b', 14)
    assert actual.data == [[11, 2, 3, None], [4, 55, 6, 14], [13, 8, 9, None]]

    # add a new column
    actual.set(13, 'd', 88)
    assert actual.data == [[11, 2, 3, None], [4, 55, 6, 14], [13, 8, 9, None], [None, None, None, 88]]

    # add a new row and column
    actual.set(14, 'e', 999)
    assert actual.data == [[11, 2, 3, None, None], [4, 55, 6, 14, None], [13, 8, 9, None, None],
                           [None, None, None, 88, None], [None, None, None, None, 999]]


def test_set_row():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    # change existing row
    actual.set(indexes=10, values={'a': 11, 'b': 44, 'c': 77})
    assert actual.data == [[11, 2, 3], [44, 5, 6], [77, 8, 9]]

    actual.set(indexes=12, values={'a': 33, 'b': 66, 'c': 99})
    assert actual.data == [[11, 2, 33], [44, 5, 66], [77, 8, 99]]

    # change subset of existing row
    actual.set(indexes=11, values={'a': 22, 'c': 88})
    assert actual.data == [[11, 22, 33], [44, 5, 66], [77, 88, 99]]

    # add a new row
    actual.set(indexes=13, values={'a': 4, 'b': 7, 'c': 10})
    assert actual.data == [[11, 22, 33, 4], [44, 5, 66, 7], [77, 88, 99, 10]]

    actual.set(indexes=14, values={'b': 8, 'c': 11})
    assert actual.data == [[11, 22, 33, 4, None], [44, 5, 66, 7, 8], [77, 88, 99, 10, 11]]
    assert actual.index == [10, 11, 12, 13, 14]

    # bad column names
    with pytest.raises(ValueError):
        actual.set(indexes=14, values={'a': 0, 'bad': 1})

    # bad values type
    with pytest.raises(TypeError):
        actual.set(indexes=14, values=[1, 2, 3, 4, 5])


def test_set_column():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    # change existing column
    actual.set(columns='b', values=[44, 55, 66])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9]]

    # add a new column
    actual.set(columns='e', values=[10, 11, 12])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9], [10, 11, 12]]

    # not enough values
    with pytest.raises(ValueError):
        actual.set(columns='e', values=[1, 2])

    # too many values
    with pytest.raises(ValueError):
        actual.set(columns='e', values=[1, 2, 3, 4])


def test_set_column_index_subset():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    # by index value
    actual.set(columns='b', indexes=[12, 11, 10], values=[66, 55, 44])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9]]

    actual.set(columns='a', indexes=[12, 10], values=[33, 11])
    assert actual.data == [[11, 2, 33], [44, 55, 66], [7, 8, 9]]

    # new rows
    actual.set(columns='c', indexes=[12, 13, 14], values=[120, 130, 140])
    assert actual.data == [[11, 2, 33, None, None], [44, 55, 66, None, None], [7, 8, 120, 130, 140]]
    assert actual.index == [10, 11, 12, 13, 14]

    # new row new columns
    actual.set(columns='z', indexes=[14, 15, 16], values=['zoo', 'boo', 'hoo'])
    assert actual.data == [[11, 2, 33, None, None, None, None], [44, 55, 66, None, None, None, None],
                           [7, 8, 120, 130, 140, None, None], [None, None, None, None, 'zoo', 'boo', 'hoo']]
    assert actual.index == [10, 11, 12, 13, 14, 15, 16]

    # values list shorter than indexes, raise error
    with pytest.raises(ValueError):
        actual.set(indexes=[10, 11], columns='a', values=[1])

    # by boolean list
    actual = rc.DataFrame({'c': [1, 2], 'a': [4, 5], 'b': [7, 8]}, index=['first', 'second'], columns=['a', 'b', 'c'])
    actual.set(columns='c', indexes=[False, True], values=[99])
    assert actual.data == [[4, 5], [7, 8], [1, 99]]

    # boolean list not size of existing index
    with pytest.raises(ValueError):
        actual.set(indexes=[True, False, True], columns='a', values=[1, 2])

    # boolean list True entries not same size as values list
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], columns='b', values=[4, 5, 6])

    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], columns='b', values=[4])


def test_set_single_value():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    # set multiple index to one value
    df.set([10, 12], 'a', 99)
    assert df.data == [[99, 2, 99], [4, 5, 6], [7, 8, 9]]

    # set entire column to one value
    df.set(columns='c', values=88)
    assert df.data == [[99, 2, 99], [4, 5, 6], [88, 88, 88]]

    # can be anything that isn't a list
    df.set(columns='e', values={1, 2, 3})
    assert df.data == [[99, 2, 99], [4, 5, 6], [88, 88, 88], [{1, 2, 3}, {1, 2, 3}, {1, 2, 3}]]


def test_set_from_blank_df():
    # single cell
    df = rc.DataFrame()
    df.set(indexes=1, columns='a', values=9)
    assert df.columns == ['a']
    assert df.index == [1]
    assert df.data == [[9]]

    # single column
    df = rc.DataFrame()
    df.set(indexes=[1, 2, 3], columns='a', values=[9, 10, 11])
    assert df.columns == ['a']
    assert df.index == [1, 2, 3]
    assert df.data == [[9, 10, 11]]


def test_set_square_brackets():
    df = rc.DataFrame()

    df[1, 'a'] = 2
    assert df.data == [[2]]

    # df[[0, 3], 'b'] - - set index = [0, 3], column = b
    df[[0, 3], 'b'] = 4
    assert df.data == [[2, None, None], [None, 4, 4]]

    # df[1:2, 'b'] - - set index slice 1:2, column = b
    df[1:3, 'b'] = 5
    assert df.data == [[2, None, None], [5, 5, 5]]


def test_bar():
    df = rc.DataFrame(columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    for x in range(10):
        df.set(indexes=x, values={'datetime': '2001-01-01', 'open': 100.0, 'high': 101.0, 'low': 99.5,
                                'close': 99.75, 'volume': 10000})

    assert df.index == list(range(10))
    assert df.columns == ['datetime', 'open', 'high', 'low', 'close', 'volume']
    assert df.data[0] == ['2001-01-01'] * 10


def test_get_cell():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    assert actual.get(10, 'a') == 1
    assert actual.get(11, 'a') == 2
    assert actual.get(12, 'c') == 9


def test_get_rows():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10')

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12], index_name='start_10')
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([11, 12], 'c', as_list=True) == [8, 9]

    # test with boolean list
    actual = df.get([False, True, True, False], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([False, True, True, False], 'c', as_list=True) == [8, 9]

    # get entire column
    assert df.get(columns='b', as_list=True) == [4, 5, 6, 7]


def test_get_columns():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10')

    expected = rc.DataFrame({'a': [4], 'c': [None]}, index=[99], columns=['a', 'c'], index_name='start_10')
    actual = df.get(99, ['a', 'c'])
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get(99, [True, False, True])
    assert_frame_equal(actual, expected)


def test_get_row_and_col():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, index=['x', 'y', 'z'],
                      columns=['a', 'b', 'c', 'd'], index_name='letters')

    expected = rc.DataFrame({'b': [4, 6], 'd': [10, 12]}, index=['x', 'z'], columns=['b', 'd'], index_name='letters')
    actual = df.get(['x', 'z'], ['b', 'd'])
    assert_frame_equal(actual, expected)

    # test with booleans
    actual = df.get([True, False, True], [False, True, False, True])
    assert_frame_equal(actual, expected)

    # get everything
    everything = df.get()
    assert_frame_equal(everything, df)


def test_get_square_brackets():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'])

    # df['b'] -- get column
    assert_frame_equal(df['b'], rc.DataFrame({'b': [4, 5, 6]}))

    # df[['a', 'b', c']] -- get columns
    assert_frame_equal(df[['a', 'b', 'c']], rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                                                         columns=['a', 'b', 'c']))

    # df[1, 'd'] -- get cell at index = 5, column = 'b'
    assert df[1, 'd'] == 11

    # df[[0, 2]] -- get indexes = [0, 2] all columns
    assert_frame_equal(df[[0, 2], df.columns],
                       rc.DataFrame({'a': [1, 3], 'b': [4, 6], 'c': [7, 9], 'd': [10, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[0, 2]))

    # df[[0, 2], 'c'] -- get indexes = [4, 5], column = 'b'
    assert_frame_equal(df[[0, 2], 'c'], rc.DataFrame({'c': [7, 9]}, index=[0, 2]))

    # df[[1, 2], ['a', 'd']] -- get indexes = [4, 5], columns = ['a', 'b']
    assert_frame_equal(df[[1, 2], ['a', 'd']], rc.DataFrame({'a': [2, 3], 'd': [11, 12]}, columns=['a', 'd'],
                       index=[1, 2]))


def test_get_slicer():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'])

    # df[1:2] -- get slice from index 1 to 2, all columns
    assert_frame_equal(df[1:2],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2]))

    # df[0:1, ['c', 'd']] -- get slice from index 0 to 1, columns ['c', 'd']
    assert_frame_equal(df[0:1, ['c', 'd']], rc.DataFrame({'c': [7, 8], 'd': [10, 11]},
                                                         columns=['c', 'd'], index=[0, 1]))

    # df[1:1, 'c'] -- get slice 1 to 1 and column 'c'
    assert_frame_equal(df[1:1, 'c'], rc.DataFrame({'c': [8]}, index=[1]))


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

    # cannot to_list on a mulit-column DataFrame
    with pytest.raises(TypeError):
        df.to_list()


def test_rename_columns():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])

    df.rename_columns({'b': 'b_new'})
    assert df.columns == ['b_new', 'a']

    df.rename_columns({'b_new': 'b2', 'a': 'a2'})
    assert df.columns == ['b2', 'a2']

    with pytest.raises(ValueError):
        df.rename_columns({'a2': 'a', 'bad': 'nogo'})


def test_head():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2])

    assert_frame_equal(df.head(0), rc.DataFrame(columns=[1, 2]))
    assert_frame_equal(df.head(1), rc.DataFrame({1: [0], 2: [3]}, columns=[1, 2]))
    assert_frame_equal(df.head(2), rc.DataFrame({1: [0, 1], 2: [3, 4]}, columns=[1, 2]))
    assert_frame_equal(df.head(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2]))
    assert_frame_equal(df.head(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2]))


def test_tail():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2])

    assert_frame_equal(df.tail(0), rc.DataFrame(columns=[1, 2]))
    assert_frame_equal(df.tail(1), rc.DataFrame({1: [2], 2: [5]}, columns=[1, 2], index=[2]))
    assert_frame_equal(df.tail(2), rc.DataFrame({1: [1, 2], 2: [4, 5]}, columns=[1, 2], index=[1, 2]))
    assert_frame_equal(df.tail(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2]))
    assert_frame_equal(df.tail(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2]))


def test_delete_row():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])

    df.delete_rows(['a', 'c'])
    assert_frame_equal(df, rc.DataFrame({'a': [2], 'b': [5]}, columns=['b', 'a'], index=['b']))

    df.delete_rows('b')
    assert_frame_equal(df, rc.DataFrame(columns=['b', 'a']))

    # insert back in data
    df[1, 'a'] = 9
    assert df.data == [[None], [9]]

    df[2, 'b'] = 8
    assert df.data == [[None, 8], [9, None]]

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    # cannot delete values not in index
    with pytest.raises(ValueError):
        df.delete_rows(['bad'])

    # length of boolean must be len of index
    with pytest.raises(ValueError):
        df.delete_rows([True, False])

    df.delete_rows([True, False, True])
    assert_frame_equal(df, rc.DataFrame({'a': [2], 'b': [5]}, columns=['b', 'a'], index=['b']))

    df.delete_rows([True])
    assert_frame_equal(df, rc.DataFrame(columns=['b', 'a']))


def test_delete_columns():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, columns=['a', 'b', 'c'])

    # cannot delete bad column
    with pytest.raises(ValueError):
        df.delete_columns(['bad', 'a'])

    df.delete_columns(['a', 'c'])
    assert_frame_equal(df, rc.DataFrame({'b': [4, 5, 6]}))
    assert df.index == [0, 1, 2]

    # insert some data back in
    df[1, 'a'] = 77
    assert df.data == [[4, 5, 6], [None, 77, None]]

    df.delete_columns(['b', 'a'])
    assert_frame_equal(df, rc.DataFrame())
    assert df.columns == []
    assert df.index == []

    # insert some data back in, fresh columns and index
    df[1, 'e'] = 77
    assert df.data == [[77]]


def test_sort_index():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[10, 8, 9])

    df.sort_index()
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': [5, 6, 4]}, columns=['a', 'b'], index=[8, 9, 10]))


def test_sort_column():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])

    # cannot sort mulitple columns
    with pytest.raises(TypeError):
        df.sort_columns(['a', 'b'])

    df.sort_columns('a')
    assert_frame_equal(df, rc.DataFrame({'a': [1, 2, 3], 'b': ['c', 'a', 'b']}, columns=['a', 'b'], index=[8, 10, 9]))

    df.sort_columns('b')
    assert_frame_equal(df, rc.DataFrame({'a': [2, 3, 1], 'b': ['a', 'b', 'c']}, columns=['a', 'b'], index=[10, 9, 8]))


def test_validate_index():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df.validate_integrity()

    # index not right length
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9, 11, 12])

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df._index = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        df.validate_integrity()

    # duplicate index
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 10, 9])

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    with pytest.raises(ValueError):
        df.index = [10, 10, 10]

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df._index = [10, 10, 9]
    with pytest.raises(ValueError):
        df.validate_integrity()


def test_validate_columns():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df.validate_integrity()

    # columns not right length
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b', 'extra'])

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'])
    df._columns = ['a', 'b', 'extra']
    with pytest.raises(ValueError):
        df.validate_integrity()

    # duplicate columns
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']})
    with pytest.raises(ValueError):
        df.columns = ['dup', 'dup']

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df._columns = ['dup', 'dup']
    with pytest.raises(ValueError):
        df.validate_integrity()


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


def test_print():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [1.0, 2.55, 3.1], 'c': ['first', 'second', None]}, columns=['b', 'c', 'a'],
                      index=['row1', 'row2', 'row3'])

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

    # print() method will pass along any argument for the tabulate.tabulate function


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

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [1.0, 2.55, 3.1]}, columns=['a', 'b'])
    assert len(df) == 3

    df['a', 3] = 99
    assert len(df) == 4


def test_equality():
    df = rc.DataFrame({'z': [1, 2, 1, 2, 1, 1]})

    assert df.equality('z', value=1) == [True, False, True, False, True, True]
    assert df.equality('z', [1, 2, 3], 2) == [True, False, True]
    assert df.equality('z', [False, False, False, True, True, True], 1) == [False, True, True]

    # change all 1 to 3
    df.set(indexes=df.equality('z', value=1), columns='z', values=3)
    assert df.data == [[3, 2, 3, 2, 3, 3]]


def test_add():
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


def test_select_index():
    # simple index
    df = rc.DataFrame({'a': [1, 2, 3, 4, 5, 6]}, index=['a', 'b', 'c', 'd', 'e', 'f'])

    actual = df.select_index('c', 'value')
    assert actual == ['c']

    actual = df.select_index('d', 'boolean')
    assert actual == [False, False, False, True, False, False]

    with pytest.raises(ValueError):
        df.select_index('a', 'BAD')

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

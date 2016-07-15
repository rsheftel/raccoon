import pytest
import raccoon as rc
from raccoon.utils import assert_frame_equal


def test_initialization():
    # solid matrix, no columns, no index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    assert set(tuple(x) for x in actual.data) == {(1, 2, 3), (4, 5, 6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == [0, 1, 2]

    # solid matrix, no columns, with index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'])
    assert set(tuple(x) for x in actual.data) == {(1, 2, 3), (4, 5, 6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == ['a', 'b', 'c']

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
    with pytest.raises(AttributeError):
        rc.DataFrame(index=[1, 2, 3])

    # wrong number in index
    with pytest.raises(AttributeError):
        rc.DataFrame({'a': [1, 2, 3]}, index=[1])

    # wrong number of columns
    with pytest.raises(AttributeError):
        rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a'])

    with pytest.raises(AttributeError):
        rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b', 'c', 'TOO', 'MANY'])

    # columns does not match dict keys
    with pytest.raises(AttributeError):
        rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['BAD', 'VALUE'])

    # index is not a list
    with pytest.raises(AttributeError):
        rc.DataFrame({'a': [1]}, index=1)

    # columns is not a list
    with pytest.raises(AttributeError):
        rc.DataFrame({'a': [1]}, columns='a')


def test_columns():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    names = actual.columns
    assert names == ['b', 'a']

    # test that a view is returned
    names.append('bad')
    assert actual.columns != ['b', 'a']

    actual.columns = ['new1', 'new2']
    assert actual.columns == ['new1', 'new2']

    with pytest.raises(AttributeError):
        actual.columns = ['list', 'too', 'long']


def test_index():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    result = actual.index
    assert result == ['a', 'b', 'c']

    # test that a view is returned
    result.append('bad')
    assert actual.index != ['a', 'b', 'c']

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]

    with pytest.raises(AttributeError):
        actual.index = [1, 3, 4, 5, 6]


def test_values():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    assert actual.data == [[4, 5, 6], [1, 2, 3]]

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
    actual.set(index=10, values={'a': 11, 'b': 44, 'c': 77})
    assert actual.data == [[11, 2, 3], [44, 5, 6], [77, 8, 9]]

    actual.set(index=12, values={'a': 33, 'b': 66, 'c': 99})
    assert actual.data == [[11, 2, 33], [44, 5, 66], [77, 8, 99]]

    # change subset of existing row
    actual.set(index=11, values={'a': 22, 'c': 88})
    assert actual.data == [[11, 22, 33], [44, 5, 66], [77, 88, 99]]

    # add a new row
    actual.set(index=13, values={'a': 4, 'b': 7, 'c': 10})
    assert actual.data == [[11, 22, 33, 4], [44, 5, 66, 7], [77, 88, 99, 10]]

    actual.set(index=14, values={'b': 8, 'c': 11})
    assert actual.data == [[11, 22, 33, 4, None], [44, 5, 66, 7, 8], [77, 88, 99, 10, 11]]
    assert actual.index == [10, 11, 12, 13, 14]

    # bad column names
    with pytest.raises(AttributeError):
        actual.set(index=14, values={'a': 0, 'bad': 1})

    # bad values type
    with pytest.raises(AttributeError):
        actual.set(index=14, values=[1, 2, 3, 4, 5])


def test_set_column():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    # change existing column
    actual.set(column='b', values=[44, 55, 66])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9]]

    # add a new column
    actual.set(column='e', values=[10, 11, 12])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9], [10, 11, 12]]

    # values list longer than index adds rows
    actual.set(column='e', values=[20, 30, 40, 50])
    assert actual.data == [[1, 2, 3, None], [44, 55, 66, None], [7, 8, 9, None], [20, 30, 40, 50]]

    # not enough values
    with pytest.raises(AttributeError):
        actual.set(column='e', values=[1, 2])

    # bad values type
    with pytest.raises(AttributeError):
        actual.set(column='e', values={1, 2, 3})


def test_set_column_index_subset():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    # by index value
    actual.set(column='b', index=[12, 11, 10], values=[66, 55, 44])
    assert actual.data == [[1, 2, 3], [44, 55, 66], [7, 8, 9]]

    actual.set(column='a', index=[12, 10], values=[33, 11])
    assert actual.data == [[11, 2, 33], [44, 55, 66], [7, 8, 9]]

    # new rows
    actual.set(column='c', index=[12, 13, 14], values=[120, 130, 140])
    assert actual.data == [[11, 2, 33, None, None], [44, 55, 66, None, None], [7, 8, 120, 130, 140]]
    assert actual.index == [10, 11, 12, 13, 14]

    # new row new columns
    actual.set(column='z', index=[14, 15, 16], values=['zoo', 'boo', 'hoo'])
    assert actual.data == [[11, 2, 33, None, None, None, None], [44, 55, 66, None, None, None, None],
                           [7, 8, 120, 130, 140, None, None], [None, None, None, None, 'zoo', 'boo', 'hoo']]
    assert actual.index == [10, 11, 12, 13, 14, 15, 16]

    # values list shorter than indexes, raise error
    with pytest.raises(AttributeError):
        actual.set(index=[10, 11], column='a', values=[1])

    # by boolean list
    actual = rc.DataFrame({'c': [1, 2], 'a': [4, 5], 'b': [7, 8]}, index=['first', 'second'], columns=['a', 'b', 'c'])
    actual.set(column='c', index=[False, True], values=[99])
    assert actual.data == [[4, 5], [7, 8], [1, 99]]

    # boolean list not size of existing index
    with pytest.raises(AttributeError):
        actual.set(index=[True, False, True], column='a', values=[1, 2])

    # boolean list True entries not same size as values list
    with pytest.raises(AttributeError):
        actual.set(index=[True, True, False], column='b', values=[4, 5, 6])

    with pytest.raises(AttributeError):
        actual.set(index=[True, True, False], column='b', values=[4])


def test_set_from_blank_df():
    # single cell
    df = rc.DataFrame()
    df.set(index=1, column='a', values=9)
    assert df.columns == ['a']
    assert df.index == [1]
    assert df.data == [[9]]

    # single column
    df = rc.DataFrame()
    df.set(index=[1, 2, 3], column='a', values=[9, 10, 11])
    assert df.columns == ['a']
    assert df.index == [1, 2, 3]
    assert df.data == [[9, 10, 11]]


def test_bar():
    df = rc.DataFrame(columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    for x in range(10):
        df.set(index=x, values={'datetime': '2001-01-01', 'open': 100.0, 'high': 101.0, 'low': 99.5,
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
                      columns=['a', 'b', 'c'])

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12])
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)


def test_get_columns():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'])

    expected = rc.DataFrame({'a': [4], 'c': [None]}, index=[99], columns=['a', 'c'])
    actual = df.get(99, ['a', 'c'])
    assert_frame_equal(actual, expected)


def test_get_row_and_col():
    pass

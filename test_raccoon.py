import pytest
from . import raccoon as rc


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


def test_jagged_data():
    actual = rc.DataFrame({'a': [], 'b': [1], 'c': [1, 2], 'd': [1, 2, 3]}, columns=['a', 'b', 'c', 'd'])
    assert actual.data == [[None, None, None], [1, None, None], [1, 2, None], [1, 2, 3]]
    assert actual.columns == ['a', 'b', 'c', 'd']
    assert actual.index == [0, 1, 2]


def test_empty_initialization():
    actual = rc.DataFrame()
    assert isinstance(actual, rc.DataFrame)
    assert actual.data == [[]]
    assert actual.columns == []
    assert actual.index == []

    actual = rc.DataFrame(columns=['a', 'b', 'c'])
    assert actual.data == [[], [], []]
    assert actual.columns == ['a', 'b', 'c']
    assert actual.index == []

    actual = rc.DataFrame(index=[1, 2, 3])
    assert actual.data == [[None, None, None]]
    assert actual.columns == [1]
    assert actual.index == [1, 2, 3]

    actual = rc.DataFrame(index=[1, 2, 3], columns=['a', 'b'])
    assert actual.data == [[None, None, None], [None, None, None]]
    assert actual.columns == ['a', 'b']
    assert actual.index == [1, 2, 3]


def test_bad_initialization():
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


def test_at():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 12], columns=['a', 'b', 'c'])

    assert actual.get(10, 'a') == 1
    assert actual.get(11, 'a') == 2
    assert actual.get(12, 'c') == 9


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

    # add a new column

    # add a new row and column


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


def test_set_column():
    pass


def test_ohlcv():
    df = rc.DataFrame(columns=['datetime', 'open', 'high','low','close','volume'])
    for x in range(10):
        df.set(index=x, values={'datetime': '2001-01-01', 'open': 100.0, 'high': 101.0, 'low': 99.5,
                                'close': 99.75, 'volume': 10000})

    assert df.index == list(range(10))
    assert df.columns == ['datetime', 'open', 'high', 'low', 'close', 'volume']
    assert df.data[0] == ['2001-01-01'] * 10

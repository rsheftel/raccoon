import pytest
import raccoon as rc
from blist import blist


def test_columns():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    names = actual.columns
    assert names == ['b', 'a']
    assert isinstance(names, list)

    # test that a copy is returned
    names.append('bad')
    assert actual.columns == ['b', 'a']

    actual.columns = ['new1', 'new2']
    assert actual.columns == ['new1', 'new2']
    assert isinstance(actual.columns, list)

    with pytest.raises(ValueError):
        actual.columns = ['list', 'too', 'long']


def test_columns_blist():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'], use_blist=True)
    names = actual.columns
    assert names == ['b', 'a']
    assert isinstance(names, blist)

    # test that a copy is returned
    names.append('bad')
    assert actual.columns == ['b', 'a']

    actual.columns = ['new1', 'new2']
    assert actual.columns == ['new1', 'new2']
    assert isinstance(actual.columns, blist)

    with pytest.raises(ValueError):
        actual.columns = ['list', 'too', 'long']


def test_index():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    result = actual.index
    assert result == ['a', 'b', 'c']
    assert isinstance(result, list)

    # test that a view is returned
    result.append('bad')
    assert actual.index == ['a', 'b', 'c', 'bad']

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]
    assert isinstance(result, list)

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]

    assert actual.index_name == 'index'
    actual.index_name = 'new name'
    assert actual.index_name == 'new name'

    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], index_name='letters')
    assert actual.index_name == 'letters'


def test_index_blist():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'], use_blist=True)
    result = actual.index
    assert result == ['a', 'b', 'c']
    assert isinstance(result, blist)

    # test that a view is returned
    result.append('bad')
    assert actual.index == ['a', 'b', 'c', 'bad']

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]
    assert isinstance(result, blist)

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]


def test_get_index():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sort=False)

    # test that then using .index returns a view
    res = df.index
    res.append(100)
    assert res == [10, 11, 12, 99, 100]
    assert df.index == [10, 11, 12, 99, 100]


def test_data():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    assert actual.data == [[4, 5, 6], [1, 2, 3]]

    # test shallow copy
    new = actual.data
    new[0][0] = 99
    assert actual.data == new
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    new.append(88)
    assert actual.data != new

    with pytest.raises(AttributeError):
        actual.data = [4, 5]


def test_data_blist():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'], use_blist=True)
    assert actual.data == [[4, 5, 6], [1, 2, 3]]
    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])

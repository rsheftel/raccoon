import pytest
import raccoon as rc
from blist import blist

import sys
PYTHON3 = (sys.version_info >= (3, 0))


def test_default_empty_init():
    actual = rc.DataFrame()
    assert isinstance(actual, rc.DataFrame)
    assert actual.data == []
    assert actual.columns == []
    assert actual.index == []
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    actual = rc.DataFrame(sort=False)
    assert actual.sort is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    actual = rc.DataFrame(columns=['a', 'b', 'c'])
    assert actual.data == [[], [], []]
    assert actual.columns == ['a', 'b', 'c']
    assert actual.index == []
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    actual = rc.DataFrame(index=[1, 2, 3], columns=['a', 'b'])
    assert actual.data == [[None, None, None], [None, None, None]]
    assert actual.columns == ['a', 'b']
    assert actual.index == [1, 2, 3]
    assert actual.sort is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    actual = rc.DataFrame(index=[1, 2, 3], columns=['a', 'b'], use_blist=True)
    assert actual.data == [[None, None, None], [None, None, None]]
    assert actual.columns == ['a', 'b']
    assert actual.index == [1, 2, 3]
    assert actual.sort is False
    assert isinstance(actual.index, blist)
    assert isinstance(actual.columns, blist)
    assert isinstance(actual.data, blist)
    assert all([isinstance(actual.data[x], blist) for x in range(len(actual.columns))])

    actual = rc.DataFrame(index=[1, 2, 3], columns=['a', 'b'], sort=True)
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])


def test_default_init():
    # solid matrix, no columns, no index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    assert set(tuple(x) for x in actual.data) == {(1, 2, 3), (4, 5, 6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == [0, 1, 2]
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    # solid matrix, no columns, with index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], index_name='letters')
    assert set(tuple(x) for x in actual.data) == {(1, 2, 3), (4, 5, 6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == ['a', 'b', 'c']
    assert actual.index_name == 'letters'
    assert actual.sort is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    # solid matrix, columns, index
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    assert actual.data == [[4, 5, 6], [1, 2, 3]]
    assert actual.columns == ['b', 'a']
    assert actual.index == ['a', 'b', 'c']
    assert actual.sort is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])

    # dict values are not lists
    actual = rc.DataFrame({'a': 1, 'b': 2, 'c': [1, 2, 3]}, columns=['b', 'c', 'a'])
    assert actual.columns == ['b', 'c', 'a']
    assert actual.index == [0, 1, 2]
    assert actual.data == [[2, None, None], [1, 2, 3], [1, None, None]]
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)
    assert isinstance(actual.data, list)
    assert all([isinstance(actual.data[x], list) for x in range(len(actual.columns))])


def test_sorted_init():
    # initialized with index defaults to False
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], index=[12, 11, 13])
    assert df.sort is False

    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], index=[12, 11, 13], sort=True)
    assert df.sort is True
    assert df.index == [11, 12, 13]
    assert df.data == [[1, 2, 3], [4, 5, 6]]

    # initialized with no index defaults to True
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'])
    assert df.sort is True
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], sort=False)
    assert df.sort is False

    # if sort is true, but no index provided it will assume already in sort order
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], sort=True)
    assert df.sort is True
    assert df.index == [0, 1, 2]
    assert df.data == [[2, 1, 3], [5, 4, 6]]

    # start un-sort, then set to sort
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, columns=['a', 'b'], index=[12, 11, 13], sort=False)
    assert df.sort is False
    assert df.index == [12, 11, 13]
    assert df.data == [[2, 1, 3], [5, 4, 6]]

    df.sort = True
    assert df.index == [11, 12, 13]
    assert df.data == [[1, 2, 3], [4, 5, 6]]

    # mixed type index will bork on sort=True
    if PYTHON3:
        with pytest.raises(TypeError):
            rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6]}, index=[1, 'b', 3], sort=True)


def test_jagged_data():
    actual = rc.DataFrame({'a': [], 'b': [1], 'c': [1, 2], 'd': [1, 2, 3]}, columns=['a', 'b', 'c', 'd'])
    assert actual.data == [[None, None, None], [1, None, None], [1, 2, None], [1, 2, 3]]
    assert actual.columns == ['a', 'b', 'c', 'd']
    assert actual.index == [0, 1, 2]
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.columns, list)


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

    # bad data type
    with pytest.raises(TypeError):
        rc.DataFrame(data=[1, 2, 3])

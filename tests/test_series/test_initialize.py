import sys
import pytest
import raccoon as rc
from blist import blist
from raccoon.utils import assert_series_equal

PYTHON3 = (sys.version_info >= (3, 0))


def test_default_empty_init():
    actual = rc.Series()
    assert isinstance(actual, rc.Series)
    assert actual.data == []
    assert actual.data_name == 'value'
    assert actual.index == []
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(sort=False)
    assert actual.sort is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(data_name='points')
    assert actual.data == []
    assert actual.data_name == 'points'
    assert actual.index == []
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(index=[1, 2, 3], data_name='points')
    assert actual.data == [None, None, None]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.sort is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(index=[1, 2, 3], data_name='points', use_blist=True)
    assert actual.data == [None, None, None]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.index_name == 'index'
    assert actual.sort is False
    assert isinstance(actual.index, blist)
    assert isinstance(actual.data, blist)

    actual = rc.Series(index=[1, 2, 3], index_name='dates', data_name='points', sort=True)
    assert actual.data == [None, None, None]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.index_name == 'dates'
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)


def test_default_init():
    # no index
    actual = rc.Series([4, 5, 6])
    assert actual.data == [4, 5, 6]
    assert actual.data_name == 'value'
    assert actual.index == [0, 1, 2]
    assert actual.sort is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)
    assert len(actual) == 3

    # with index
    actual = rc.Series(data=[4, 5, 6], index=['a', 'b', 'c'], index_name='letters')
    assert actual.data == [4, 5, 6]
    assert actual.index == ['a', 'b', 'c']
    assert actual.index_name == 'letters'
    assert actual.sort is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)
    assert len(actual) == 3


def test_views():
    # assert that df.data is data and df.index are copies and do not alter input data
    data = [4, 5, 6]
    index = ['a', 'b', 'c']
    actual = rc.Series(data=data, index=index)

    assert actual.data is not data
    assert actual.index is not index

    # change input data, no change to series
    data.append(7)
    index.append('e')

    assert actual.data == [4, 5, 6]
    assert actual.index == ['a', 'b', 'c']


def test_sorted_init():
    # initialized with index defaults to False
    df = rc.Series([5, 4, 6], index=[12, 11, 13])
    assert df.sort is False

    df = rc.Series([5, 4, 6], index=[12, 11, 13], sort=True)
    assert df.sort is True
    assert df.index == [11, 12, 13]
    assert df.data == [4, 5, 6]

    # initialized with no index defaults to True
    df = rc.Series([5, 4, 6])
    assert df.sort is True
    df = rc.Series([5, 4, 6], sort=False)
    assert df.sort is False

    # if sort is true, but no index provided it will assume already in sort order
    df = rc.Series([5, 4, 6], sort=True)
    assert df.sort is True
    assert df.index == [0, 1, 2]
    assert df.data == [5, 4, 6]

    # start un-sort, then set to sort
    df = rc.Series([5, 4, 6], index=[12, 11, 13], sort=False)
    assert df.sort is False
    assert df.index == [12, 11, 13]
    assert df.data == [5, 4, 6]

    df.sort = True
    assert df.index == [11, 12, 13]
    assert df.data == [4, 5, 6]

    # mixed type index will bork on sort=True
    if PYTHON3:
        with pytest.raises(TypeError):
            rc.Series([5, 4, 6], index=[1, 'b', 3], sort=True)


def test_bad_initialization():
    # wrong length of index
    with pytest.raises(ValueError):
        rc.Series([1, 2, 3], index=[1])

    with pytest.raises(ValueError):
        rc.Series(data=[2], index=['b', 'c', 'a'])

    # index is not a list
    with pytest.raises(TypeError):
        rc.Series({'a': [1]}, index=1)

    # bad data type
    with pytest.raises(TypeError):
        rc.Series(data=(1, 2, 3))

    with pytest.raises(TypeError):
        rc.Series(data={'data': [1, 2, 3]})

    # index not a list
    with pytest.raises(TypeError):
        rc.Series(data=[2], index='b')

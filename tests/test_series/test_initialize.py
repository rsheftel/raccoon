import pytest
import raccoon as rc
from blist import blist

import sys

PYTHON3 = (sys.version_info >= (3, 0))


def test_default_empty_init():
    actual = rc.Series()
    assert isinstance(actual, rc.Series)
    assert actual.data == []
    assert actual.data_name == 'value'
    assert actual.index == []
    assert actual.sorted is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(sorted=False)
    assert actual.sorted is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(data_name='points')
    assert actual.data == []
    assert actual.data_name == 'points'
    assert actual.index == []
    assert actual.sorted is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(index=[1, 2, 3], data_name='points')
    assert actual.data == [None, None, None]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.sorted is False
    assert actual.offset == 0
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    actual = rc.Series(index=[1, 2, 3], data_name='points', use_blist=True, offset=1)
    assert actual.data == [None, None, None]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.index_name == 'index'
    assert actual.sorted is False
    assert actual.offset == 1
    assert isinstance(actual.index, blist)
    assert isinstance(actual.data, blist)

    actual = rc.Series(index=[1, 2, 3], index_name='dates', data_name='points', sorted=True)
    assert actual.data == [None, None, None]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.index_name == 'dates'
    assert actual.sorted is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)


def test_default_init():
    # no index
    actual = rc.Series([4, 5, 6])
    assert actual.data == [4, 5, 6]
    assert actual.data_name == 'value'
    assert actual.index == [0, 1, 2]
    assert actual.sorted is True
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)

    # with index
    actual = rc.Series(data=[4, 5, 6], index=['a', 'b', 'c'], index_name='letters')
    assert actual.data == [4, 5, 6]
    assert actual.index == ['a', 'b', 'c']
    assert actual.index_name == 'letters'
    assert actual.sorted is False
    assert isinstance(actual.index, list)
    assert isinstance(actual.data, list)


def test_views():
    # assert that df.data is data and df.index is index because they are views not copies
    data = [4, 5, 6]
    index = ['a', 'b', 'c']
    actual = rc.Series(data=data, index=index)

    assert actual.data is data
    assert actual.index is index

    # does NOT work if use_blist is different from what is passed in (ie: pass in list, but use_blist=True)
    data = [4, 5, 6]
    index = ['a', 'b', 'c']
    actual = rc.Series(data=data, index=index, use_blist=True)

    assert actual.data is not data
    assert actual.index is not index


def test_sorted_init():
    # initialized with index defaults to False
    df = rc.Series([5, 4, 6], index=[12, 11, 13])
    assert df.sorted is False

    df = rc.Series([5, 4, 6], index=[12, 11, 13], sorted=True)
    assert df.sorted is True
    assert df.index == [11, 12, 13]
    assert df.data == [4, 5, 6]

    # initialized with no index defaults to True
    df = rc.Series([5, 4, 6])
    assert df.sorted is True
    df = rc.Series([5, 4, 6], sorted=False)
    assert df.sorted is False

    # if sorted is true, but no index provided it will assume already in sorted order
    df = rc.Series([5, 4, 6], sorted=True)
    assert df.sorted is True
    assert df.index == [0, 1, 2]
    assert df.data == [5, 4, 6]

    # start un-sorted, then set to sorted
    df = rc.Series([5, 4, 6], index=[12, 11, 13], sorted=False)
    assert df.sorted is False
    assert df.index == [12, 11, 13]
    assert df.data == [5, 4, 6]

    df.sorted = True
    assert df.index == [11, 12, 13]
    assert df.data == [4, 5, 6]

    # mixed type index will bork on sorted=True
    if PYTHON3:
        with pytest.raises(TypeError):
            rc.Series([5, 4, 6], index=[1, 'b', 3], sorted=True)


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

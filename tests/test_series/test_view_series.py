import pytest
import raccoon as rc
from blist import blist

import sys


def test_default_empty_init():
    actual = rc.ViewSeries(data=[4, 5, 6], index=[1, 2, 3])
    assert actual.data == [4, 5, 6]
    assert actual.data_name == 'value'
    assert actual.index == [1, 2, 3]
    assert actual.index_name == 'index'
    assert actual.sort is False
    assert actual.offset == 0

    actual = rc.ViewSeries(data=[4, 5, 6], index=[1, 2, 3], data_name='points', offset=1)
    assert actual.data == [4, 5, 6]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.index_name == 'index'
    assert actual.sort is False
    assert actual.offset == 1

    actual = rc.ViewSeries(data=[4, 5, 6], index=[1, 2, 3], index_name='dates', data_name='points', sort=True)
    assert actual.data == [4, 5, 6]
    assert actual.data_name == 'points'
    assert actual.index == [1, 2, 3]
    assert actual.index_name == 'dates'
    assert actual.sort is True


def test_views():
    # assert that df.data is data and df.index are copies and do not alter input data
    data = [4, 5, 6]
    index = ['a', 'b', 'c']
    actual = rc.ViewSeries(data=data, index=index)

    assert actual.data is data
    assert actual.index is index

    # change input data, no change to ViewSeries
    data.append(7)
    index.append('e')

    assert actual.data == [4, 5, 6, 7]
    assert actual.index == ['a', 'b', 'c', 'e']
    assert actual.data is data
    assert actual.index is index


def test_sorted_init():
    # sorted always defaults to False
    df = rc.ViewSeries([5, 4, 6], index=[12, 11, 13])
    assert df.sort is False

    # initializing with sort does not change the data or index. The sort is a flag to speed up gets
    df = rc.ViewSeries([5, 4, 6], index=[12, 11, 13], sort=True)
    assert df.sort is True
    assert df.index == [12, 11, 13]
    assert df.data == [5, 4, 6]

    # cannot change sort status
    df = rc.ViewSeries([5, 4, 6], index=[12, 11, 13], sort=False)
    with pytest.raises(NotImplementedError):
        df.sort = True


def test_bad_initialization():
    # cannot initialize empty
    with pytest.raises(ValueError):
        rc.ViewSeries()

    # data with no index not allowed
    with pytest.raises(ValueError):
        rc.ViewSeries(data=[1, 2, 3])

    # index with no data not allowed
    with pytest.raises(ValueError):
        rc.ViewSeries(index=[1, 2, 3])

    # wrong length of index
    with pytest.raises(ValueError):
        rc.ViewSeries([1, 2, 3], index=[1])

    with pytest.raises(ValueError):
        rc.ViewSeries(data=[2], index=['b', 'c', 'a'])

    # index is not a list
    with pytest.raises(TypeError):
        rc.ViewSeries({'a': [1]}, index=1)

    # bad data type
    with pytest.raises(TypeError):
        rc.ViewSeries(data=(1, 2, 3), index=[4, 5, 6])

    with pytest.raises(TypeError):
        rc.ViewSeries(data={'data': [1, 2, 3]}, index=[4, 5, 6])

    # index not a list
    with pytest.raises(TypeError):
        rc.ViewSeries(data=[2], index='b')


def test_not_implemented():
    """
    These are all the tests that are implemented in the Series class that are not in ViewSeries
    """
    ser = rc.ViewSeries(data=[4, 5, 6], index=[1, 2, 3])

    with pytest.raises(NotImplementedError):
       ser.blist

    with pytest.raises(NotImplementedError):
       ser.sort = True

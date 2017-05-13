import raccoon as rc
from raccoon.utils import assert_series_equal
import pytest


def test_get_cell():
    actual = rc.Series([1, 2, 3], index=[10, 11, 13], sort=False)

    assert actual.get(10) == 1
    assert actual.get(11) == 2
    assert actual.get(13) == 3

    # test items not in index raise errors
    with pytest.raises(ValueError):
        actual.get(1)

    with pytest.raises(ValueError):
        actual.get(100)

    with pytest.raises(ValueError):
        actual.get(12)


def test_get_cell_sorted():
    actual = rc.Series([1, 2, 3], index=[10, 11, 13], sort=True)

    assert actual.get(10) == 1
    assert actual.get(11) == 2
    assert actual.get(13) == 3

    # test items not in index raise errors
    with pytest.raises(ValueError):
        actual.get(1)

    with pytest.raises(ValueError):
        actual.get(100)

    with pytest.raises(ValueError):
        actual.get(12)


def test_get_rows():
    srs = rc.Series([1, 2, 3, 4], index=[10, 11, 12, 99], index_name='start_10', sort=False)

    expected = rc.Series([2, 3], index=[11, 12], index_name='start_10', sort=False)
    actual = srs.get([11, 12])
    assert_series_equal(actual, expected)

    # test with boolean list
    actual = srs.get([False, True, True, False])
    assert_series_equal(actual, expected)

    # index out of order
    expected = rc.Series([4, 1], index=[99, 10], index_name='start_10', sort=False)
    actual = srs.get([99, 10])
    assert_series_equal(actual, expected)

    # get as a list
    assert srs.get([11, 12], as_list=True) == [2, 3]

    # get as a list
    assert srs.get([False, True, True, False], as_list=True) == [2, 3]

    # items not in index raise errors
    with pytest.raises(ValueError):
        srs.get([11, 88], as_list=True)

    # not enough items in boolean list
    with pytest.raises(ValueError):
        srs.get([True, True])


def test_get_rows_sorted():
    srs = rc.Series([1, 2, 3, 4], index=[10, 11, 12, 99], index_name='start_10', sort=True)

    expected = rc.Series([2, 3], index=[11, 12], index_name='start_10', sort=True)
    actual = srs.get([11, 12])
    assert_series_equal(actual, expected)

    # test with boolean list
    actual = srs.get([False, True, True, False])
    assert_series_equal(actual, expected)

    # index out of order
    expected = rc.Series([4, 1], index=[99, 10], index_name='start_10', sort=True)
    actual = srs.get([99, 10])
    assert_series_equal(actual, expected)

    # get as a list
    assert srs.get([11, 12], as_list=True) == [2, 3]

    # get as a list
    assert srs.get([False, True, True, False], as_list=True) == [2, 3]

    # items not in index raise errors
    with pytest.raises(ValueError):
        srs.get([11, 88], as_list=True)

    # not enough items in boolean list
    with pytest.raises(ValueError):
        srs.get([True, True])


def test_get_location():
    srs = rc.Series([5, 6, 7, 8], index=[2, 4, 6, 8])

    assert srs.get_location(2) == {'value': 7, 'index': 6}
    assert srs.get_location(-1) == {'index': 8, 'value': 8}


def test_get_locations():
    srs = rc.Series([5, 6, 7, 8], index=[2, 4, 6, 8])

    assert_series_equal(srs.get_locations([0, 2]), rc.Series([5, 7], index=[2, 6]))
    assert srs.get_locations([0, 2], as_list=True) == [5, 7]
    assert_series_equal(srs.get_locations([2]), rc.Series([7], index=[6]))


def test_get_slice():
    srs = rc.Series([5, 6, 7, 8], index=[2, 4, 6, 8], sort=True)

    assert_series_equal(srs.get_slice(2, 8), srs)
    assert_series_equal(srs.get_slice(1, 8), srs)
    assert_series_equal(srs.get_slice(2, 18), srs)
    assert_series_equal(srs.get_slice(1, 18), srs)

    assert_series_equal(srs.get_slice(4, 4), rc.Series([6], [4], sort=True))
    assert_series_equal(srs.get_slice(3, 4), rc.Series([6], [4], sort=True))
    assert_series_equal(srs.get_slice(4, 5), rc.Series([6], [4], sort=True))
    assert_series_equal(srs.get_slice(3, 5), rc.Series([6], [4], sort=True))

    assert_series_equal(srs.get_slice(3, 6), rc.Series([6, 7], [4, 6], sort=True))
    assert_series_equal(srs.get_slice(4, 7), rc.Series([6, 7], [4, 6], sort=True))
    assert_series_equal(srs.get_slice(3, 7), rc.Series([6, 7], [4, 6], sort=True))

    assert_series_equal(srs.get_slice(None, 7), rc.Series([5, 6, 7], [2, 4, 6], sort=True))
    assert_series_equal(srs.get_slice(3, None), rc.Series([6, 7, 8], [4, 6, 8], sort=True))

    assert_series_equal(srs.get_slice(3, 3), rc.Series([], [], sort=True))
    assert_series_equal(srs.get_slice(0, 0), rc.Series([], [], sort=True))
    assert_series_equal(srs.get_slice(5, 5), rc.Series([], [], sort=True))

    # Only works with sort=True
    with pytest.raises(RuntimeError):
        rc.Series([4, 5], [6, 7], sort=False).get_slice(6, 6)


def test_get_slice_as_list():
    srs = rc.Series([5, 6, 7, 8], index=[2, 4, 6, 8], sort=True)

    assert srs.get_slice(2, 8, as_list=True) == ([2, 4, 6, 8], [5, 6, 7, 8])
    assert srs.get_slice(1, 8, as_list=True) == ([2, 4, 6, 8], [5, 6, 7, 8])
    assert srs.get_slice(2, 18, as_list=True) == ([2, 4, 6, 8], [5, 6, 7, 8])
    assert srs.get_slice(1, 18, as_list=True) == ([2, 4, 6, 8], [5, 6, 7, 8])

    assert srs.get_slice(4, 4, as_list=True) == ([4], [6])
    assert srs.get_slice(3, 4, as_list=True) == ([4], [6])
    assert srs.get_slice(4, 5, as_list=True) == ([4], [6])
    assert srs.get_slice(3, 5, as_list=True) == ([4], [6])

    assert srs.get_slice(3, 6, as_list=True) == ([4, 6], [6, 7])
    assert srs.get_slice(4, 7, as_list=True) == ([4, 6], [6, 7])
    assert srs.get_slice(3, 7, as_list=True) == ([4, 6], [6, 7])

    assert srs.get_slice(None, 7, as_list=True) == ([2, 4, 6], [5, 6, 7])
    assert srs.get_slice(3, None, as_list=True) == ([4, 6, 8], [6, 7, 8])

    assert srs.get_slice(3, 3, as_list=True) == ([], [])
    assert srs.get_slice(0, 0, as_list=True) == ([], [])
    assert srs.get_slice(5, 5, as_list=True) == ([], [])


def test_get_square_brackets():
    srs = rc.Series([10, 11, 12], index=['a', 'b', 'c'], sort=False)

    assert srs['b'] == 11
    assert_series_equal(srs[['a', 'c']], rc.Series([10, 12], ['a', 'c']))

    # get a series back
    assert_series_equal(srs[['b']], rc.Series([11], ['b'], sort=False))

    assert_series_equal(srs[['c', 'a']], rc.Series([12, 10], ['c', 'a'], sort=False))

    # srs[[0, 2]] -- get indexes = [0, 2]
    srs = rc.Series([10, 11, 12], sort=False)
    assert_series_equal(srs[[0, 2]], rc.Series([10, 12], index=[0, 2], sort=False))

    assert_series_equal(srs[[2, 1]], rc.Series([12, 11], index=[2, 1], sort=False))


def test_get_square_brackets_sorted():
    srs = rc.Series([10, 11, 12], index=['a', 'b', 'c'], sort=True)

    assert srs['b'] == 11
    assert_series_equal(srs[['a', 'c']], rc.Series([10, 12], ['a', 'c'], sort=True))

    # get a series back
    assert_series_equal(srs[['b']], rc.Series([11], ['b'], sort=True))

    assert_series_equal(srs[['c', 'a']], rc.Series([12, 10], ['c', 'a'], sort=True))

    # srs[[0, 2]] -- get indexes = [0, 2]
    srs = rc.Series([10, 11, 12], sort=True)
    assert_series_equal(srs[[0, 2]], rc.Series([10, 12], index=[0, 2], sort=True))

    assert_series_equal(srs[[2, 1]], rc.Series([12, 11], index=[2, 1], sort=True))


def test_get_slicer():
    srs = rc.Series([7, 8, 9], index=[1, 2, 3], sort=False)

    assert_series_equal(srs[2:3], rc.Series([8, 9], index=[2, 3], sort=False))
    assert_series_equal(srs[1:2], rc.Series([7, 8], index=[1, 2], sort=False))
    assert_series_equal(srs[2:2], rc.Series([8], index=[2], sort=False))

    # test indexes not in the range
    with pytest.raises(IndexError):
        _ = srs[4:5]

    with pytest.raises(IndexError):
        _ = srs[1:8]

    with pytest.raises(IndexError):
        _ = srs[2:1]


def test_get_slicer_sorted():
    srs = rc.Series([7, 8, 9], index=[1, 2, 3], sort=True)

    assert_series_equal(srs[2:3], rc.Series([8, 9], index=[2, 3], sort=True))
    assert_series_equal(srs[1:2], rc.Series([7, 8], index=[1, 2], sort=True))
    assert_series_equal(srs[0.5:2.5], rc.Series([7, 8], index=[1, 2], sort=True))
    assert_series_equal(srs[2:2], rc.Series([8], index=[2], sort=True))

    assert_series_equal(srs[4:5], rc.Series([], index=[], sort=True))
    assert_series_equal(srs[2:1], rc.Series([], index=[], sort=True))
    assert_series_equal(srs[1:8], srs)


def test_head():
    srs = rc.Series([3, 4, 5], sort=False)

    assert_series_equal(srs.head(0), rc.Series([], [], sort=False))
    assert_series_equal(srs.head(1), rc.Series([3], sort=False))
    assert_series_equal(srs.head(2), rc.Series([3, 4], sort=False))
    assert_series_equal(srs.head(3), rc.Series([3, 4, 5], sort=False))
    assert_series_equal(srs.head(999), rc.Series([3, 4, 5], sort=False))


def test_tail():
    srs = rc.Series([3, 4, 5], sort=False)

    assert_series_equal(srs.tail(0), rc.Series([], [], sort=False))
    assert_series_equal(srs.tail(1), rc.Series([5], index=[2], sort=False))
    assert_series_equal(srs.tail(2), rc.Series([4, 5], index=[1, 2], sort=False))
    assert_series_equal(srs.tail(3), rc.Series([3, 4, 5], sort=False))
    assert_series_equal(srs.tail(999), rc.Series([3, 4, 5], sort=False))

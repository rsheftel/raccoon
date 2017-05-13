import pytest
import raccoon as rc
from raccoon.utils import assert_series_equal

import sys
PYTHON3 = (sys.version_info >= (3, 0))


def test_set_cell():
    actual = rc.Series([4, 5, 6], index=[10, 11, 12], sort=False)

    # change existing value
    actual.set(11, 55)
    assert actual.get(11) == 55
    actual.set(10, 11)
    assert actual.get(10) == 11
    actual.set(10, 13)
    assert actual.get(10) == 13
    assert actual.data == [13, 55, 6]

    # add a new row
    actual.set(13, 14)
    assert actual.data == [13, 55, 6, 14]

    # add a new row note that index does not sort
    actual.set(1, -100)
    assert actual.data == [13, 55, 6, 14, -100]
    assert actual.index == [10, 11, 12, 13, 1]


def test_set_cell_sort():
    actual = rc.Series([7, 8, 9], index=[10, 12, 13], sort=True)

    # change existing value
    actual.set(12, 55)
    assert actual.get(12) == 55
    actual.set(10, 11)
    assert actual.get(10) == 11
    actual.set(10, 13)
    assert actual.get(10) == 13
    assert actual.data == [13, 55, 9]

    # add a new row
    actual.set(14, 15)
    assert actual.index == [10, 12, 13, 14]
    assert actual.data == [13, 55, 9, 15]

    # row in the middle
    actual.set(11, -1)
    assert actual.index == [10, 11, 12, 13, 14]
    assert actual.data == [13, -1, 55, 9, 15]

    # add before beginning
    actual.set(5, 999)
    assert actual.index == [5, 10, 11, 12, 13, 14]
    assert actual.data == [999, 13, -1, 55, 9, 15]

    # fails for mixed index type
    if PYTHON3:
        with pytest.raises(TypeError):
            actual.set('Z', 60)


def test_set_rows():
    actual = rc.Series([7, 8, 9], index=[10, 11, 12], sort=False)

    # change some of the values
    actual.set([11, 12], [88, 99])
    assert actual.data == [7, 88, 99]

    # change all existing values
    actual.set(actual.index, values=[44, 55, 66])
    assert actual.data == [44, 55, 66]

    # modify existing and add a new row
    actual.set([12, 9], [666, 77])
    assert actual.data == [44, 55, 666, 77]
    assert actual.index == [10, 11, 12, 9]

    # only add a new row
    actual.set([8], [5])
    assert actual.data == [44, 55, 666, 77, 5]
    assert actual.index == [10, 11, 12, 9, 8]

    # not enough values
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, True], values=[1, 2])

    # number of values must equal number of True indexes
    with pytest.raises(ValueError):
        actual.set(indexes=[True, False, True, False, False], values=[1, 2, 3])

    # too many values
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, True, True], values=[1, 2, 3, 4])


def test_set_rows_sort():
    actual = rc.Series([7, 8, 9], index=[10, 11, 12], sort=True)

    # change some of the values
    actual.set([11, 12], [88, 99])
    assert actual.data == [7, 88, 99]

    # change all existing values
    actual.set(actual.index, values=[44, 55, 66])
    assert actual.data == [44, 55, 66]

    # modify existing and add a new row
    actual.set([12, 9, 10.5], [666, 77, 1])
    assert actual.data == [77, 44, 1, 55, 666]
    assert actual.index == [9, 10, 10.5, 11, 12]

    # only add a new row
    actual.set([8], [5])
    assert actual.data == [5, 77, 44, 1, 55, 666]
    assert actual.index == [8, 9, 10, 10.5, 11, 12]

    # not enough values
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, True], values=[1, 2])

    # number of values must equal number of True indexes
    with pytest.raises(ValueError):
        actual.set(indexes=[True, False, True], values=[1, 2, 3])

    # too many values
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, True, True], values=[1, 2, 3, 4])


def test_set_index_subset():
    actual = rc.Series([7, 8, 9], index=[10, 11, 12], sort=False)

    # by index value
    actual.set(indexes=[12, 11, 10], values=[66, 55, 44])
    assert actual.data == [44, 55, 66]

    actual.set(indexes=[12, 10], values=[33, 11])
    assert actual.data == [11, 55, 33]

    # new rows
    actual.set(indexes=[12, 13, 14], values=[120, 130, 140])
    assert actual.data == [11, 55, 120, 130, 140]
    assert actual.index == [10, 11, 12, 13, 14]

    # values list shorter than indexes, raise error
    with pytest.raises(ValueError):
        actual.set(indexes=[10, 11], values=[1])

    # by boolean list
    actual = rc.Series([7, 8], index=['first', 'second'], sort=False)
    actual.set(indexes=[False, True], values=[99])
    assert actual.data == [7, 99]

    # boolean list not size of existing index
    with pytest.raises(ValueError):
        actual.set(indexes=[True, False, True], values=[1, 2])

    # boolean list True entries not same size as values list
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], values=[4, 5, 6])

    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], values=[4])


def test_set_index_subset_sort():
    actual = rc.Series([1, 2, 3], index=[10, 11, 12], sort=True)

    # by index value
    actual.set(indexes=[12, 11, 10], values=[66, 55, 44])
    assert actual.data == [44, 55, 66]

    actual.set(indexes=[12, 10], values=[33, 11])
    assert actual.data == [11, 55, 33]

    # new rows at end
    actual.set(indexes=[12, 14, 15], values=[120, 130, 140])
    assert actual.data == [11, 55, 120, 130, 140]
    assert actual.index == [10, 11, 12, 14, 15]

    # new rows at beginning
    actual.set(indexes=[10, 4, 5], values=[-140, -120, -130])
    assert actual.data == [-120, -130, -140, 55, 120, 130, 140]
    assert actual.index == [4, 5, 10, 11, 12, 14, 15]

    # new rows in middle
    actual.set(indexes=[13, 6], values=[3131, 6060])
    assert actual.data == [-120, -130, 6060, -140, 55, 120, 3131, 130, 140]
    assert actual.index == [4, 5, 6, 10, 11, 12, 13, 14, 15]

    # new row new columns
    actual.set(indexes=[14, 15, 16], values=['zoo', 'boo', 'hoo'])
    assert actual.index == [4, 5, 6, 10, 11, 12, 13, 14, 15, 16]
    assert actual.data == [-120, -130, 6060, -140, 55, 120, 3131, 'zoo', 'boo', 'hoo']

    # values list shorter than indexes, raise error
    with pytest.raises(ValueError):
        actual.set(indexes=[10, 11], values=[1])

    # by boolean list
    actual = rc.Series([1, 2], index=['first', 'second'], sort=True)
    actual.set(indexes=[False, True], values=[99])
    assert actual.data == [1, 99]

    # boolean list not size of existing index
    with pytest.raises(ValueError):
        actual.set(indexes=[True, False, True], values=[1, 2])

    # boolean list True entries not same size as values list
    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], values=[4, 5, 6])

    with pytest.raises(ValueError):
        actual.set(indexes=[True, True, False], values=[4])


def test_set_single_value():
    srs = rc.Series([4, 5, 6], index=[10, 11, 12], sort=False)

    # set multiple index to one value
    srs.set([10, 12], 99)
    assert srs.data == [99, 5, 99]


def test_set_location():
    srs = rc.Series([5, 6, 7, 8], index=[2, 4, 6, 8])

    srs.set_location(0, -1)
    assert_series_equal(srs, rc.Series([-1, 6, 7, 8], index=[2, 4, 6, 8]))

    srs.set_location(3, -10)
    assert_series_equal(srs, rc.Series([-1, 6, 7, -10], index=[2, 4, 6, 8]))

    with pytest.raises(IndexError):
        srs.set_location(5, 9)


def test_set_locations():
    srs = rc.Series([5, 6, 7, 8], index=[2, 4, 6, 8])

    srs.set_locations([0, 2], [-1, -3])
    assert_series_equal(srs, rc.Series([-1, 6, -3, 8], index=[2, 4, 6, 8]))

    srs.set_locations([1, 3], -10)
    assert_series_equal(srs, rc.Series([-1, -10, -3, -10], index=[2, 4, 6, 8]))

    with pytest.raises(IndexError):
        srs.set_locations([1, 10], [9, 99])


def test_set_from_blank_srs():
    # single cell
    srs = rc.Series(sort=False)
    srs.set(indexes=1, values=9)
    assert srs.index == [1]
    assert srs.data == [9]

    # single column
    srs = rc.Series(sort=False)
    srs.set(indexes=[1, 2, 3], values=[9, 10, 11])
    assert srs.index == [1, 2, 3]
    assert srs.data == [9, 10, 11]


def test_set_square_brackets():
    srs = rc.Series(sort=False)

    srs[1] = 2
    assert srs.data == [2]
    assert srs.index == [1]

    # srs[[0, 3]] - - set index = [0, 3]
    srs[[0, 3]] = 4
    assert srs.data == [2, 4, 4]
    assert srs.index == [1, 0, 3]

    # srs[1:2] - - set index slice 1:2
    srs[1:3] = 5
    assert srs.data == [5, 5, 5]
    assert srs.index == [1, 0, 3]
    assert srs.sort is False

    # with sort = True
    srs = rc.Series(sort=True)

    srs[1] = 2
    assert srs.data == [2]
    assert srs.index == [1]

    # srs[[0, 3]] - - set index = [0, 3]
    srs[[0, 3]] = 4
    assert srs.data == [4, 2, 4]
    assert srs.index == [0, 1, 3]

    # srs[1:2] - - set index slice 1:2
    srs[1:3] = 5
    assert srs.data == [4, 5, 5]
    assert srs.index == [0, 1, 3]
    assert srs.sort is True

    # insert
    srs[2] = 6
    assert srs.data == [4, 5, 6, 5]
    assert srs.index == [0, 1, 2, 3]


def test_append_row():
    actual = rc.Series([7, 9], index=[10, 12], sort=False)

    actual.append_row(9, 99)
    expected = rc.Series([7, 9, 99], index=[10, 12, 9])
    assert_series_equal(actual, expected)

    actual.append_row(16, 100)
    expected = rc.Series([7, 9, 99, 100], index=[10, 12, 9, 16])
    assert_series_equal(actual, expected)

    with pytest.raises(IndexError):
        actual.append_row(10, 100)


def test_append_rows():
    actual = rc.Series([7, 9], index=[10, 12], sort=False)

    actual.append_rows([9, 11], [99, 100])
    expected = rc.Series([7, 9, 99, 100], index=[10, 12, 9, 11])
    assert_series_equal(actual, expected)

    actual.append_rows([16, 17], [110, 120])
    expected = rc.Series([7, 9, 99, 100, 110, 120], index=[10, 12, 9, 11, 16, 17])
    assert_series_equal(actual, expected)

    with pytest.raises(IndexError):
        actual.append_rows([1, 10], [100, 110])

    with pytest.raises(ValueError):
        actual.append_rows([1, 10], [100, 110, 120])

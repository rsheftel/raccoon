import pytest
import raccoon as rc
from raccoon.utils import assert_series_equal


def test_delete():
    srs = rc.Series([1, 2, 3], index=['a', 'b', 'c'])

    srs.delete(['a', 'c'])
    assert_series_equal(srs, rc.Series([2], index=['b']))

    srs.delete('b')
    assert_series_equal(srs, rc.Series(sort=False))

    # insert back in data
    srs[1] = 9
    assert srs.data == [9]
    assert srs.index == [1]

    srs[2] = 8
    assert srs.data == [9, 8]
    assert srs.index == [1, 2]

    srs = rc.Series([4, 5, 6], index=['a', 'b', 'c'])
    # cannot delete values not in index
    with pytest.raises(ValueError):
        srs.delete(['bad'])

    # length of boolean must be len of index
    with pytest.raises(ValueError):
        srs.delete([True, False])

    srs.delete([True, False, True])
    assert_series_equal(srs, rc.Series([5], index=['b']))

    srs.delete([True])
    assert_series_equal(srs, rc.Series(sort=False))


def test_delete_sort():
    srs = rc.Series([4, 5, 6], index=['a', 'b', 'c'], sort=True, use_blist=False)

    srs.delete(['a', 'c'])
    assert_series_equal(srs, rc.Series([5], index=['b'], sort=True, use_blist=False))

    srs.delete('b')
    assert_series_equal(srs, rc.Series(sort=True, use_blist=False))

    # insert back in data
    srs[2] = 9
    assert srs.data == [9]
    assert srs.index == [2]

    srs[1] = 8
    assert srs.data == [8, 9]
    assert srs.index == [1, 2]

    srs = rc.Series([4, 5, 6], index=['a', 'b', 'c'])
    # cannot delete values not in index
    with pytest.raises(ValueError):
        srs.delete(['bad'])

    # length of boolean must be len of index
    with pytest.raises(ValueError):
        srs.delete([True, False])

    srs.delete([True, False, True])
    assert_series_equal(srs, rc.Series([5], index=['b']))

    srs.delete([True])
    assert_series_equal(srs, rc.Series(sort=False))

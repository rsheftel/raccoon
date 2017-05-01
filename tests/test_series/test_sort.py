import sys
import pytest
import raccoon as rc
from raccoon.utils import assert_series_equal
from blist import blist

PYTHON3 = (sys.version_info >= (3, 0))


def test_sort_index():
    # test on list
    srs = rc.Series([4, 5, 6], index=[10, 8, 9], sort=False)

    srs.sort_index()
    assert isinstance(srs.index, list)
    assert_series_equal(srs, rc.Series([5, 6, 4], index=[8, 9, 10], sort=False))

    # test on blist
    srs = rc.Series([4, 5, 6], index=[10, 8, 9], sort=False, use_blist=True)

    srs.sort_index()
    assert isinstance(srs.index, blist)
    assert_series_equal(srs, rc.Series([5, 6, 4], index=[8, 9, 10], sort=False, use_blist=True))

    # fails on mixed type columns
    srs = rc.Series([4, 5, 6], index=[10, 'a', 9])
    if PYTHON3:
        with pytest.raises(TypeError):
            srs.sort_index()


def test_sort_multi_index():
    srs = rc.Series([4, 5, 6], index=[(10, 'c'), (10, 'a'), (10, 'b')], sort=False)

    srs.sort_index()
    assert isinstance(srs.index, list)
    assert_series_equal(srs, rc.Series([5, 6, 4], index=[(10, 'a'), (10, 'b'), (10, 'c')], sort=False))

    # fails on mixed type columns
    srs = rc.Series([4, 5, 6], index=[(10, 'c'), 'a', (10, 'b')])
    if PYTHON3:
        with pytest.raises(TypeError):
            srs.sort_index()

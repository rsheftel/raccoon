"""
unit tests for utils module
"""

import raccoon as rc
from raccoon.utils import assert_series_equal
import pytest


def test_assert_series_equal():
    srs1 = rc.Series([1, 2, 3], index=[1, 2, 3])
    assert_series_equal(srs1, srs1)

    srs2 = rc.Series([1, 1, 1], index=[1, 2, 3])
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    srs2 = rc.Series([1, 2, 3], index=[11, 12, 13])
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    srs2 = rc.Series([1, 2, 3], index=[1, 2, 3], use_blist=True)
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    srs2 = rc.Series([1, 2, 3], index=[1, 2, 3], sort=True)
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    # View Series
    srs1 = rc.ViewSeries([1, 2, 3], index=[1, 2, 3])
    assert_series_equal(srs1, srs1)

    srs2 = rc.ViewSeries([1, 1, 1], index=[1, 2, 3])
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    srs2 = rc.ViewSeries([1, 2, 3], index=[1, 2, 3], offset=9)
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    srs2 = rc.ViewSeries([1, 2, 3], index=[11, 12, 13])
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    srs2 = rc.ViewSeries([1, 2, 3], index=[1, 2, 3], sort=True)
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)


def test_data_function():
    # Example function for testing
    def assert_approx_equal(left_data, right_data, precision=0.00001):
        for i in range(len(left_data)):
            assert abs(left_data[i]- right_data[i]) <= precision

    srs1 = rc.Series([1.0, 3.0], index=[1, 3])
    srs2 = rc.Series([1.0, 3.001], index=[1, 3])

    # confirm fails with standard compare
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2)

    # passes with function and proper parameters
    assert_series_equal(srs1, srs2, assert_approx_equal, {'precision': 0.01})

    # fails with function and precision parameter to low
    with pytest.raises(AssertionError):
        assert_series_equal(srs1, srs2, assert_approx_equal, {'precision': 0.00001})

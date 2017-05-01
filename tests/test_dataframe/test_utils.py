"""
unit tests for utils module
"""

import raccoon as rc
from raccoon.utils import assert_frame_equal
import pytest


def test_assert_frame_equal():
    df1 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3])
    assert_frame_equal(df1, df1)

    df2 = rc.DataFrame({'a': [1, 1, 1], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3])
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['b', 'a'], index=[1, 2, 3])
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[11, 12, 13])
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3], use_blist=True)
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    df2 = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, columns=['a', 'b'], index=[1, 2, 3], sort=True)
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)


def test_data_function():
    # Example function for testing
    def assert_approx_equal(left_data, right_data, precision=0.00001):
        for i in range(len(left_data)):
            for j in range(len(left_data[i])):
                assert abs(left_data[i][j]- right_data[i][j]) <= precision

    df1 = rc.DataFrame({'a': [1.0, 3.0], 'b': [4.0, 6.0]}, columns=['a', 'b'], index=[1, 3])
    df2 = rc.DataFrame({'a': [1.0, 3.001], 'b': [4.0, 6.001]}, columns=['a', 'b'], index=[1, 3])

    # confirm fails with standard compare
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2)

    # passes with function and proper parameters
    assert_frame_equal(df1, df2, assert_approx_equal, {'precision': 0.01})

    # fails with function and precision parameter to low
    with pytest.raises(AssertionError):
        assert_frame_equal(df1, df2, assert_approx_equal, {'precision': 0.00001})

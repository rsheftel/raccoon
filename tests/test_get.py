import raccoon as rc
from raccoon.utils import assert_frame_equal
import pytest


def test_get_cell():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 13], columns=['a', 'b', 'c'],
                          sorted=False)

    assert actual.get(10, 'a') == 1
    assert actual.get(11, 'a') == 2
    assert actual.get(13, 'c') == 9

    # test items not in index raise errors
    with pytest.raises(ValueError):
        actual.get(1, 'a')

    with pytest.raises(ValueError):
        actual.get(100, 'a')

    with pytest.raises(ValueError):
        actual.get(12, 'a')


def test_get_cell_sorted():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 13], columns=['a', 'b', 'c'],
                          sorted=True)

    assert actual.get(10, 'a') == 1
    assert actual.get(11, 'a') == 2
    assert actual.get(13, 'c') == 9

    # test items not in index raise errors
    with pytest.raises(ValueError):
        actual.get(1, 'a')

    with pytest.raises(ValueError):
        actual.get(100, 'a')

    with pytest.raises(ValueError):
        actual.get(12, 'a')


def test_get_rows():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sorted=False)

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12], index_name='start_10', sorted=False)
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([11, 12], 'c', as_list=True) == [8, 9]

    # test with boolean list
    actual = df.get([False, True, True, False], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([False, True, True, False], 'c', as_list=True) == [8, 9]

    # get entire column
    assert df.get(columns='b', as_list=True) == [4, 5, 6, 7]

    # items not in index raise errors
    with pytest.raises(ValueError):
        df.get([11, 88], 'c', as_list=True)

    # not enough items in boolean list
    with pytest.raises(ValueError):
        df.get([True, True], 'c')


def test_get_rows_sorted():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sorted=True)

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12], index_name='start_10', sorted=False)
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([11, 12], 'c', as_list=True) == [8, 9]

    # test with boolean list
    actual = df.get([False, True, True, False], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([False, True, True, False], 'c', as_list=True) == [8, 9]

    # get entire column
    assert df.get(columns='b', as_list=True) == [4, 5, 6, 7]

    # items not in index raise errors
    with pytest.raises(ValueError):
        df.get([11, 88], 'c', as_list=True)

    # not enough items in boolean list
    with pytest.raises(ValueError):
        df.get([True, True], 'c')


def test_get_columns():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sorted=False)

    expected = rc.DataFrame({'a': [4], 'c': [None]}, index=[99], columns=['a', 'c'], index_name='start_10',
                            sorted=False)
    actual = df.get(99, ['a', 'c'])
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get(99, [True, False, True])
    assert_frame_equal(actual, expected)


def test_get_matrix():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, index=['x', 'y', 'z'],
                      columns=['a', 'b', 'c', 'd'], index_name='letters', sorted=False)

    expected = rc.DataFrame({'b': [4, 6], 'd': [10, 12]}, index=['x', 'z'], columns=['b', 'd'], index_name='letters',
                            sorted=False)
    actual = df.get(['x', 'z'], ['b', 'd'])
    assert_frame_equal(actual, expected)

    # test with booleans
    actual = df.get([True, False, True], [False, True, False, True])
    assert_frame_equal(actual, expected)

    # get everything
    everything = df.get()
    assert_frame_equal(everything, df)


def test_get_square_brackets():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sorted=False)

    # df['b'] -- get column
    assert_frame_equal(df['b'], rc.DataFrame({'b': [4, 5, 6]}, sorted=False))

    # df[['a', 'b', c']] -- get columns
    assert_frame_equal(df[['a', 'b', 'c']], rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                                                         columns=['a', 'b', 'c'], sorted=False))

    # df[1, 'd'] -- get cell at index = 5, column = 'b'
    assert df[1, 'd'] == 11

    # df[[0, 2]] -- get indexes = [0, 2] all columns
    assert_frame_equal(df[[0, 2], df.columns],
                       rc.DataFrame({'a': [1, 3], 'b': [4, 6], 'c': [7, 9], 'd': [10, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[0, 2], sorted=False))

    # df[[0, 2], 'c'] -- get indexes = [4, 5], column = 'b'
    assert_frame_equal(df[[0, 2], 'c'], rc.DataFrame({'c': [7, 9]}, index=[0, 2], sorted=False))

    # df[[1, 2], ['a', 'd']] -- get indexes = [4, 5], columns = ['a', 'b']
    assert_frame_equal(df[[1, 2], ['a', 'd']], rc.DataFrame({'a': [2, 3], 'd': [11, 12]}, columns=['a', 'd'],
                       index=[1, 2], sorted=False))


def test_get_slicer():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sorted=False)

    # df[1:2] -- get slice from index 1 to 2, all columns
    assert_frame_equal(df[1:2],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2], sorted=False))

    # df[0:1, ['c', 'd']] -- get slice from index 0 to 1, columns ['c', 'd']
    assert_frame_equal(df[0:1, ['c', 'd']], rc.DataFrame({'c': [7, 8], 'd': [10, 11]},
                                                         columns=['c', 'd'], index=[0, 1], sorted=False))

    # df[1:1, 'c'] -- get slice 1 to 1 and column 'c'
    assert_frame_equal(df[1:1, 'c'], rc.DataFrame({'c': [8]}, index=[1], sorted=False))


def test_head():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False)

    assert_frame_equal(df.head(0), rc.DataFrame(columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(1), rc.DataFrame({1: [0], 2: [3]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(2), rc.DataFrame({1: [0, 1], 2: [3, 4]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.head(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))


def test_tail():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False)

    assert_frame_equal(df.tail(0), rc.DataFrame(columns=[1, 2], sorted=False))
    assert_frame_equal(df.tail(1), rc.DataFrame({1: [2], 2: [5]}, columns=[1, 2], index=[2], sorted=False))
    assert_frame_equal(df.tail(2), rc.DataFrame({1: [1, 2], 2: [4, 5]}, columns=[1, 2], index=[1, 2], sorted=False))
    assert_frame_equal(df.tail(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))
    assert_frame_equal(df.tail(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sorted=False))

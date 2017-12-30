import raccoon as rc
from raccoon.utils import assert_frame_equal
import pytest


def test_get_cell():
    actual = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}, index=[10, 11, 13], columns=['a', 'b', 'c'],
                          sort=False)

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
                          sort=True)

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
                      columns=['a', 'b', 'c'], index_name='start_10', sort=False)

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12], index_name='start_10', sort=False)
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get([False, True, True, False], 'c')
    assert_frame_equal(actual, expected)

    # index out of order
    expected = rc.DataFrame({'c': [None, 7]}, index=[99, 10], index_name='start_10', sort=False)
    actual = df.get([99, 10], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([11, 12], 'c', as_list=True) == [8, 9]

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
                      columns=['a', 'b', 'c'], index_name='start_10', sort=True)

    expected = rc.DataFrame({'c': [8, 9]}, index=[11, 12], index_name='start_10', sort=True)
    actual = df.get([11, 12], 'c')
    assert_frame_equal(actual, expected)

    # get as a list
    assert df.get([11, 12], 'c', as_list=True) == [8, 9]

    # test with boolean list
    actual = df.get([False, True, True, False], 'c')
    assert_frame_equal(actual, expected)

    # index out of order
    expected = rc.DataFrame({'c': [7, None]}, index=[10, 99], index_name='start_10', sort=True)
    actual = df.get([99, 10], 'c')
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
                      columns=['a', 'b', 'c'], index_name='start_10', sort=False)

    # no columns given
    expected = rc.DataFrame({'a': [4], 'b': [7], 'c': [None]}, index=[99], columns=['a', 'b', 'c'],
                            index_name='start_10', sort=False)
    actual = df.get_columns(99)
    assert_frame_equal(actual, expected)

    # specific columns
    expected = rc.DataFrame({'a': [4], 'c': [None]}, index=[99], columns=['a', 'c'], index_name='start_10',
                            sort=False)
    actual = df.get(99, ['a', 'c'])
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get(99, [True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'c': [8], 'b': [5]}, index=[11], columns=['c', 'b'], index_name='start_10',
                            sort=False)
    actual = df.get(11, ['c', 'b'])
    assert_frame_equal(actual, expected)

    # as_dict
    assert df.get(11, ['b', 'c'], as_dict=True) == {'start_10': 11, 'b': 5, 'c': 8}
    assert df.get_columns(11, ['b', 'c'], as_dict=True) == {'start_10': 11, 'b': 5, 'c': 8}

    # test boolean list not same length as columns
    with pytest.raises(ValueError):
        df.get(99, [True, False])

    # test index out of bounds
    with pytest.raises(ValueError):
        df.get(88, ['a', 'c'])


def test_get_columns_sorted():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [4, 5, 6, 7], 'c': [7, 8, 9, None]}, index=[10, 11, 12, 99],
                      columns=['a', 'b', 'c'], index_name='start_10', sort=True)

    expected = rc.DataFrame({'a': [4], 'c': [None]}, index=[99], columns=['a', 'c'], index_name='start_10',
                            sort=True)
    actual = df.get(99, ['a', 'c'])
    assert_frame_equal(actual, expected)

    # test with boolean list
    actual = df.get(99, [True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'c': [8], 'b': [5]}, index=[11], columns=['c', 'b'], index_name='start_10',
                            sort=True)
    actual = df.get(11, ['c', 'b'])
    assert_frame_equal(actual, expected)

    # test boolean list not same length as columns
    with pytest.raises(ValueError):
        df.get(99, [True, False])

    # test index out of bounds
    with pytest.raises(ValueError):
        df.get(88, ['a', 'c'])


def test_get_matrix():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, index=['x', 'y', 'z'],
                      columns=['a', 'b', 'c', 'd'], index_name='letters', sort=False)

    expected = rc.DataFrame({'b': [4, 6], 'd': [10, 12]}, index=['x', 'z'], columns=['b', 'd'], index_name='letters',
                            sort=False)
    actual = df.get(['x', 'z'], ['b', 'd'])
    assert_frame_equal(actual, expected)

    # test with booleans
    actual = df.get([True, False, True], [False, True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'d': [10, 12], 'c': [7, 9]}, index=['x', 'z'], columns=['d', 'c'], index_name='letters',
                            sort=False)
    actual = df.get(['x', 'z'], ['d', 'c'])
    assert_frame_equal(actual, expected)

    # get everything
    everything = df.get()
    assert_frame_equal(everything, df)

    # boolean list does not match index length
    with pytest.raises(ValueError):
        df.get([True, False], [False, True, False, True])

    # boolean list does not match columns length
    with pytest.raises(ValueError):
        df.get([True, False, True], [False, True])

    # missing index
    with pytest.raises(ValueError):
        df.get_matrix(['BAD', 'x'], ['a', 'b'])

    # missing column
    with pytest.raises(ValueError):
        df.get_matrix(['x', 'y'], ['a', 'b', 'BAD'])


def test_get_matrix_sorted():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': [5, 4, 6], 'c': [8, 7, 9], 'd': [11, 10, 12]}, index=['y', 'x', 'z'],
                      columns=['a', 'b', 'c', 'd'], index_name='letters', sort=True)

    expected = rc.DataFrame({'b': [4, 6], 'd': [10, 12]}, index=['x', 'z'], columns=['b', 'd'], index_name='letters',
                            sort=True)
    actual = df.get(['x', 'z'], ['b', 'd'])
    assert_frame_equal(actual, expected)

    # test with booleans
    actual = df.get([True, False, True], [False, True, False, True])
    assert_frame_equal(actual, expected)

    # columns out of order
    expected = rc.DataFrame({'d': [10, 12], 'c': [7, 9]}, index=['x', 'z'], columns=['d', 'c'], index_name='letters',
                            sort=True)
    actual = df.get(['x', 'z'], ['d', 'c'])
    assert_frame_equal(actual, expected)

    # get everything
    everything = df.get()
    assert_frame_equal(everything, df)

    # boolean list does not match index length
    with pytest.raises(ValueError):
        df.get([True, False], [False, True, False, True])

    # boolean list does not match columns length
    with pytest.raises(ValueError):
        df.get([True, False, True], [False, True])

    # missing index
    with pytest.raises(ValueError):
        df.get_matrix(['BAD', 'x'], ['a', 'b'])

    # missing column
    with pytest.raises(ValueError):
        df.get_matrix(['x', 'y'], ['a', 'b', 'BAD'])


def test_get_location():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, index=[2, 4, 6, 8])

    # forward indexing, all columns
    assert_frame_equal(df.get_location(2), rc.DataFrame({'a': [3], 'b': [7]}, index=[6]))
    assert df.get_location(2, as_dict=True) == {'index': 6, 'a': 3, 'b': 7}
    assert df.get_location(2, as_dict=True, index=False) == {'a': 3, 'b': 7}

    # reverse indexing, all columns
    assert_frame_equal(df.get_location(-1), rc.DataFrame({'a': [4], 'b': [8]}, index=[8]))
    assert df.get_location(-1, as_dict=True) == {'index': 8, 'a': 4, 'b': 8}
    assert df.get_location(-1, as_dict=True, index=False) == {'a': 4, 'b': 8}

    # forward indexing, one column
    assert_frame_equal(df.get_location(0, ['a']), rc.DataFrame({'a': [1]}, index=[2]))
    assert df.get_location(0, ['a'], as_dict=True) == {'index': 2, 'a': 1}
    assert df.get_location(0, ['a'], as_dict=True, index=False) == {'a': 1}

    # reverse indexing, all columns
    assert_frame_equal(df.get_location(-2, ['b']), rc.DataFrame({'b': [7]}, index=[6]))
    assert df.get_location(-2, ['b'], as_dict=True) == {'index': 6, 'b': 7}
    assert df.get_location(-2, ['b'], as_dict=True, index=False) == {'b': 7}

    # single value for column and not list returns just the value
    assert df.get_location(1, 'b') == 6


def test_get_locations():
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, index=[2, 4, 6, 8])

    # multi row, multi columns
    assert_frame_equal(df.get_locations([0, 2]), rc.DataFrame({'a': [1, 3], 'b': [5, 7]}, index=[2, 6]))

    # multiple rows, single columns
    assert_frame_equal(df.get_locations([1, 3], 'a'), rc.DataFrame({'a': [2, 4]}, index=[4, 8]))
    assert df.get_locations([0, 2], 'b', as_list=True) == [5, 7]

    # single row, multiple columns
    assert_frame_equal(df.get_locations([2]), rc.DataFrame({'a': [3], 'b': [7]}, index=[6]))


def test_get_slice():
    # fails for non-sort DataFrame
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, index=[2, 4, 6, 8])
    with pytest.raises(RuntimeError):
        df.get_slice(2, 4)

    # empty DataFrame
    df = rc.DataFrame(sort=True)
    assert_frame_equal(df.get_slice(3, 3), rc.DataFrame(sort=True))

    df = rc.DataFrame(sort=True, columns=['a', 'b'])
    assert_frame_equal(df.get_slice(3, 3), rc.DataFrame(sort=True, columns=['a', 'b']))

    # full DataFrame
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, columns=['a', 'b'], index=[2, 4, 6, 8], sort=True)

    assert_frame_equal(df.get_slice(2, 8), df)
    assert_frame_equal(df.get_slice(1, 8), df)
    assert_frame_equal(df.get_slice(2, 10), df)
    assert_frame_equal(df.get_slice(1, 10), df)

    assert_frame_equal(df.get_slice(4, 4, ['b']), rc.DataFrame({'b': [6]}, index=[4], sort=True))
    assert_frame_equal(df.get_slice(3, 4, ['b']), rc.DataFrame({'b': [6]}, index=[4], sort=True))
    assert_frame_equal(df.get_slice(4, 5, ['b']), rc.DataFrame({'b': [6]}, index=[4], sort=True))
    assert_frame_equal(df.get_slice(3, 5, ['b']), rc.DataFrame({'b': [6]}, index=[4], sort=True))

    assert_frame_equal(df.get_slice(4, 6, ['a']), rc.DataFrame({'a': [2, 3]}, index=[4, 6], sort=True))
    assert_frame_equal(df.get_slice(3, 6, ['a']), rc.DataFrame({'a': [2, 3]}, index=[4, 6], sort=True))
    assert_frame_equal(df.get_slice(4, 7, ['a']), rc.DataFrame({'a': [2, 3]}, index=[4, 6], sort=True))
    assert_frame_equal(df.get_slice(3, 7, ['a']), rc.DataFrame({'a': [2, 3]}, index=[4, 6], sort=True))

    assert_frame_equal(df.get_slice(None, 5, ['a']), rc.DataFrame({'a': [1, 2]}, index=[2, 4], sort=True))
    assert_frame_equal(df.get_slice(5, None, [True, False]), rc.DataFrame({'a': [3, 4]}, index=[6, 8], sort=True))

    # boolean column list not the right size
    with pytest.raises(ValueError):
        df.get_slice(5, None, [True])

    assert_frame_equal(df.get_slice(3, 3), rc.DataFrame({'a': [], 'b': []}, columns=['a', 'b'], sort=True))
    assert_frame_equal(df.get_slice(0, 0), rc.DataFrame({'a': [], 'b': []}, columns=['a', 'b'], sort=True))
    assert_frame_equal(df.get_slice(10, 10), rc.DataFrame({'a': [], 'b': []}, columns=['a', 'b'], sort=True))


def test_get_slice_as_dict():
    # fails for non-sort DataFrame
    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, index=[2, 4, 6, 8])
    with pytest.raises(RuntimeError):
        df.get_slice(2, 4)

    df = rc.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]}, index=[2, 4, 6, 8], sort=True)

    assert df.get_slice(2, 8, as_dict=True) == ([2, 4, 6, 8], {'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
    assert df.get_slice(1, 8, as_dict=True) == ([2, 4, 6, 8], {'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
    assert df.get_slice(2, 10, as_dict=True) == ([2, 4, 6, 8], {'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
    assert df.get_slice(1, 10, as_dict=True) == ([2, 4, 6, 8], {'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})

    assert df.get_slice(4, 4, ['b'], as_dict=True) == ([4], {'b': [6]})
    assert df.get_slice(3, 4, ['b'], as_dict=True) == ([4], {'b': [6]})
    assert df.get_slice(4, 5, ['b'], as_dict=True) == ([4], {'b': [6]})
    assert df.get_slice(3, 5, ['b'], as_dict=True) == ([4], {'b': [6]})

    assert df.get_slice(4, 6, ['a'], as_dict=True) == ([4, 6], {'a': [2, 3]})
    assert df.get_slice(3, 6, ['a'], as_dict=True) == ([4, 6], {'a': [2, 3]})
    assert df.get_slice(4, 7, ['a'], as_dict=True) == ([4, 6], {'a': [2, 3]})
    assert df.get_slice(3, 7, ['a'], as_dict=True) == ([4, 6], {'a': [2, 3]})

    assert df.get_slice(None, 5, ['a'], as_dict=True) == ([2, 4], {'a': [1, 2]})
    assert df.get_slice(5, None, ['a'], as_dict=True) == ([6, 8], {'a': [3, 4]})

    assert df.get_slice(3, 3, as_dict=True) == ([], {'a': [], 'b': []})
    assert df.get_slice(0, 0, as_dict=True) == ([], {'a': [], 'b': []})
    assert df.get_slice(10, 10, as_dict=True) == ([], {'a': [], 'b': []})


def test_get_square_brackets():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sort=False)

    # df['b'] -- get column
    assert_frame_equal(df['b'], rc.DataFrame({'b': [4, 5, 6]}, sort=False))

    # df[['a', 'b', c']] -- get columns
    assert_frame_equal(df[['a', 'b', 'c']], rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                                                         columns=['a', 'b', 'c'], sort=False))

    assert_frame_equal(df[['c', 'a']], rc.DataFrame({'c': [7, 8, 9], 'a': [1, 2, 3]}, columns=['c', 'a'], sort=False))

    # df[1, 'd'] -- get cell at index = 5, column = 'b'
    assert df[1, 'd'] == 11

    # df[[0, 2]] -- get indexes = [0, 2] all columns
    assert_frame_equal(df[[0, 2], df.columns],
                       rc.DataFrame({'a': [1, 3], 'b': [4, 6], 'c': [7, 9], 'd': [10, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[0, 2], sort=False))

    assert_frame_equal(df[[2, 1], df.columns],
                       rc.DataFrame({'a': [3, 2], 'b': [6, 5], 'c': [9, 8], 'd': [12, 11]},
                                    columns=['a', 'b', 'c', 'd'], index=[2, 1], sort=False))

    # df[[0, 2], 'c'] -- get indexes = [4, 5], column = 'b'
    assert_frame_equal(df[[0, 2], 'c'], rc.DataFrame({'c': [7, 9]}, index=[0, 2], sort=False))

    assert_frame_equal(df[[2, 0], 'c'], rc.DataFrame({'c': [9, 7]}, index=[2, 0], sort=False))

    # df[[1, 2], ['a', 'd']] -- get indexes = [4, 5], columns = ['a', 'b']
    assert_frame_equal(df[[1, 2], ['a', 'd']], rc.DataFrame({'a': [2, 3], 'd': [11, 12]}, columns=['a', 'd'],
                                                            index=[1, 2], sort=False))

    assert_frame_equal(df[[2, 0], ['d', 'a']], rc.DataFrame({'d': [12, 10], 'a': [3, 1]}, columns=['d', 'a'],
                                                            index=[2, 0], sort=False))


def test_get_square_brackets_sorted():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sort=True)

    # df['b'] -- get column
    assert_frame_equal(df['b'], rc.DataFrame({'b': [4, 5, 6]}, sort=True))

    # df[['a', 'b', c']] -- get columns
    assert_frame_equal(df[['a', 'b', 'c']], rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]},
                                                         columns=['a', 'b', 'c'], sort=True))

    assert_frame_equal(df[['c', 'a']], rc.DataFrame({'c': [7, 8, 9], 'a': [1, 2, 3]}, columns=['c', 'a'], sort=True))

    # df[1, 'd'] -- get cell at index = 5, column = 'b'
    assert df[1, 'd'] == 11

    # df[[0, 2]] -- get indexes = [0, 2] all columns
    assert_frame_equal(df[[0, 2], df.columns],
                       rc.DataFrame({'a': [1, 3], 'b': [4, 6], 'c': [7, 9], 'd': [10, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[0, 2], sort=True))

    assert_frame_equal(df[[2, 1], df.columns],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2], sort=True))

    # df[[0, 2], 'c'] -- get indexes = [4, 5], column = 'b'
    assert_frame_equal(df[[0, 2], 'c'], rc.DataFrame({'c': [7, 9]}, index=[0, 2], sort=True))

    assert_frame_equal(df[[2, 0], 'c'], rc.DataFrame({'c': [9, 7]}, index=[2, 0], sort=True))

    # df[[1, 2], ['a', 'd']] -- get indexes = [4, 5], columns = ['a', 'b']
    assert_frame_equal(df[[1, 2], ['a', 'd']], rc.DataFrame({'a': [2, 3], 'd': [11, 12]}, columns=['a', 'd'],
                                                            index=[1, 2], sort=True))

    assert_frame_equal(df[[2, 0], ['d', 'a']], rc.DataFrame({'d': [10, 12], 'a': [1, 3]}, columns=['d', 'a'],
                                                            index=[0, 2], sort=True))


def test_get_slicer():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sort=False)

    # df[1:2] -- get slice from index 1 to 2, all columns
    assert_frame_equal(df[1:2],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2], sort=False))

    # df[0:1, ['c', 'd']] -- get slice from index 0 to 1, columns ['c', 'd']
    assert_frame_equal(df[0:1, ['c', 'd']], rc.DataFrame({'c': [7, 8], 'd': [10, 11]},
                                                         columns=['c', 'd'], index=[0, 1], sort=False))

    assert_frame_equal(df[0:1, ['d', 'c']], rc.DataFrame({'d': [10, 11], 'c': [7, 8]},
                                                         columns=['d', 'c'], index=[0, 1], sort=False))

    # df[1:1, 'c'] -- get slice 1 to 1 and column 'c'
    assert_frame_equal(df[1:1, 'c'], rc.DataFrame({'c': [8]}, index=[1], sort=False))

    # test indexes not in the range
    with pytest.raises(IndexError):
        x = df[4:5, 'c']

    with pytest.raises(IndexError):
        x = df[0:8, 'c']

    with pytest.raises(IndexError):
        x = df[2:1, 'c']


def test_get_slicer_sorted():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9], 'd': [10, 11, 12]}, columns=['a', 'b', 'c', 'd'],
                      sort=True)

    # df[1:2] -- get slice from index 1 to 2, all columns
    assert_frame_equal(df[1:2],
                       rc.DataFrame({'a': [2, 3], 'b': [5, 6], 'c': [8, 9], 'd': [11, 12]},
                                    columns=['a', 'b', 'c', 'd'], index=[1, 2], sort=True))

    # df[0:1, ['c', 'd']] -- get slice from index 0 to 1, columns ['c', 'd']
    assert_frame_equal(df[0:1, ['c', 'd']], rc.DataFrame({'c': [7, 8], 'd': [10, 11]},
                                                         columns=['c', 'd'], index=[0, 1], sort=True))

    assert_frame_equal(df[0:1, ['d', 'c']], rc.DataFrame({'d': [10, 11], 'c': [7, 8]},
                                                         columns=['d', 'c'], index=[0, 1], sort=True))

    # df[1:1, 'c'] -- get slice 1 to 1 and column 'c'
    assert_frame_equal(df[1:1, 'c'], rc.DataFrame({'c': [8]}, index=[1], sort=True))

    # test indexes not in the range
    assert_frame_equal(df[4:5], rc.DataFrame(columns=['a', 'b', 'c', 'd'], sort=True))
    assert_frame_equal(df[2:1], rc.DataFrame(columns=['a', 'b', 'c', 'd'], sort=True))
    assert_frame_equal(df[0:8], df)
    assert_frame_equal(df[1.5:3.5], df.get_slice(1.5, 3.5))


def test_head():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sort=False)

    assert_frame_equal(df.head(0), rc.DataFrame(columns=[1, 2], sort=False))
    assert_frame_equal(df.head(1), rc.DataFrame({1: [0], 2: [3]}, columns=[1, 2], sort=False))
    assert_frame_equal(df.head(2), rc.DataFrame({1: [0, 1], 2: [3, 4]}, columns=[1, 2], sort=False))
    assert_frame_equal(df.head(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sort=False))
    assert_frame_equal(df.head(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sort=False))


def test_tail():
    df = rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sort=False)

    assert_frame_equal(df.tail(0), rc.DataFrame(columns=[1, 2], sort=False))
    assert_frame_equal(df.tail(1), rc.DataFrame({1: [2], 2: [5]}, columns=[1, 2], index=[2], sort=False))
    assert_frame_equal(df.tail(2), rc.DataFrame({1: [1, 2], 2: [4, 5]}, columns=[1, 2], index=[1, 2], sort=False))
    assert_frame_equal(df.tail(3), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sort=False))
    assert_frame_equal(df.tail(999), rc.DataFrame({1: [0, 1, 2], 2: [3, 4, 5]}, columns=[1, 2], sort=False))

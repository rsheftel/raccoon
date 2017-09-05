import pytest
import raccoon as rc
from raccoon.utils import assert_series_equal


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
    # sort always defaults to False
    df = rc.ViewSeries([5, 4, 6], index=[12, 11, 13])
    assert df.sort is False

    # initializing with sort does not change the data or index. The sort is a flag to speed up gets
    df = rc.ViewSeries([5, 4, 6], index=[12, 11, 13], sort=True)
    assert df.sort is True
    assert df.index == [12, 11, 13]
    assert df.data == [5, 4, 6]

    # cannot change sort status
    df = rc.ViewSeries([5, 4, 6], index=[12, 11, 13], sort=False)
    with pytest.raises(AttributeError):
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

    with pytest.raises(AttributeError):
        ser.blist

    with pytest.raises(AttributeError):
        ser.sort = True

    with pytest.raises(AttributeError):
        ser.sort_index()

    with pytest.raises(AttributeError):
        ser.set(1, 2)

    with pytest.raises(AttributeError):
        ser.delete(1)


def test_from_dataframe():
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 9])
    actual = rc.ViewSeries.from_dataframe(df, 'b')
    expected = rc.ViewSeries([4, 5, 6], data_name='b', index=['a', 'b', 9])
    assert_series_equal(actual, expected)

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 'e'], sort=True, index_name='date')
    actual = rc.ViewSeries.from_dataframe(df, 'a', -1)
    expected = rc.ViewSeries([1, 2, 3], data_name='a', index=['a', 'b', 'e'], sort=True, offset=-1, index_name='date')
    assert_series_equal(actual, expected)

    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 9], use_blist=True)
    actual = rc.ViewSeries.from_dataframe(df, 'b')
    expected = rc.ViewSeries([4, 5, 6], data_name='b', index=['a', 'b', 9])
    assert_series_equal(actual, expected)


def test_from_series():
    srs = rc.Series(data=[4, 5, 6], index=['a', 'b', 9], data_name='b')
    actual = rc.ViewSeries.from_series(srs)
    expected = rc.ViewSeries([4, 5, 6], data_name='b', index=['a', 'b', 9])
    assert_series_equal(actual, expected)

    srs = rc.Series(data=[1, 2, 3], data_name='a', index=['a', 'b', 'e'], sort=True, index_name='date')
    actual = rc.ViewSeries.from_series(srs, -1)
    expected = rc.ViewSeries([1, 2, 3], data_name='a', index=['a', 'b', 'e'], sort=True, offset=-1, index_name='date')
    assert_series_equal(actual, expected)

    srs = rc.Series(data=[4, 5, 6], data_name='b', index=['a', 'b', 9], use_blist=True)
    actual = rc.ViewSeries.from_series(srs)
    expected = rc.ViewSeries([4, 5, 6], data_name='b', index=['a', 'b', 9])
    assert_series_equal(actual, expected)


def test_from_df_view():
    # sort = False
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['a', 'b', 9], sort=False)
    srs = rc.ViewSeries.from_dataframe(df, 'b')
    assert srs.sort is False
    assert srs.index is df.index
    assert srs.data is df.get_entire_column('b', True)

    # change cell
    df['a', 'b'] = 22
    assert srs.data == [22, 5, 6]
    assert srs.index == ['a', 'b', 9]

    # add a row
    df[11, 'b'] = -88
    assert srs.data == [22, 5, 6, -88]
    assert srs.index == ['a', 'b', 9, 11]

    # append row
    df.append_row(12, {'a': 55, 'b': 77})
    assert srs.data == [22, 5, 6, -88, 77]
    assert srs.index == ['a', 'b', 9, 11, 12]

    # sort = True
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=[0, 1, 5], sort=True)
    srs = rc.ViewSeries.from_dataframe(df, 'a')
    assert srs.sort is True
    assert srs.index is df.index
    assert srs.data is df.get_entire_column('a', True)

    # change cell
    df[1, 'a'] = 22
    assert srs.data == [1, 22, 3]
    assert srs.index == [0, 1, 5]

    # add a row end
    df[6, 'a'] = 4
    assert srs.data == [1, 22, 3, 4]
    assert srs.index == [0, 1, 5, 6]

    # add value in middle
    df[2, 'a'] = 12
    assert srs.data == [1, 22, 12, 3, 4]
    assert srs.index == [0, 1, 2, 5, 6]

    # append row
    df.append_row(7, {'a': 55, 'b': 77})
    assert srs.data == [1, 22, 12, 3, 4, 55]
    assert srs.index == [0, 1, 2, 5, 6, 7]


def test_from_df_view_breaks():
    # These actions will break the view link between the DataFrame and the ViewSeries

    # changing index
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=[0, 1, 5], sort=True)
    srs = rc.ViewSeries.from_dataframe(df, 'a')
    assert srs.index is df.index
    assert srs.data is df.get_entire_column('a', True)

    df.index = [1, 2, 3]
    assert srs.index is not df.index
    assert srs.data is df.get_entire_column('a', True)

    # sorting index
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=[0, 1, 5], sort=True)
    srs = rc.ViewSeries.from_dataframe(df, 'a')
    assert srs.index is df.index
    assert srs.data is df.get_entire_column('a', True)

    df.sort_index()
    assert srs.index is not df.index
    assert srs.data is not df.get_entire_column('a', True)

    # sorting column
    df = rc.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=[0, 1, 5], sort=True)
    srs = rc.ViewSeries.from_dataframe(df, 'a')
    assert srs.index is df.index
    assert srs.data is df.get_entire_column('a', True)

    df.sort_columns('b')
    assert srs.index is not df.index
    assert srs.data is not df.get_entire_column('a', True)


def test_from_series_view():
    # sort = False
    ins = rc.Series(data=[4, 5, 6], data_name='b', index=['a', 'b', 9], sort=False)
    srs = rc.ViewSeries.from_series(ins)
    assert srs.sort is False
    assert srs.index is srs.index
    assert srs.data is ins.data

    # change cell
    ins['a'] = 22
    assert srs.data == [22, 5, 6]
    assert srs.index == ['a', 'b', 9]

    # add a row
    ins[11] = -88
    assert srs.data == [22, 5, 6, -88]
    assert srs.index == ['a', 'b', 9, 11]

    # append row
    ins.append_row(12, 77)
    assert srs.data == [22, 5, 6, -88, 77]
    assert srs.index == ['a', 'b', 9, 11, 12]

    # sort = True
    ins = rc.Series(data=[1, 2, 3], data_name='a', index=[0, 1, 5], sort=True)
    srs = rc.ViewSeries.from_series(ins)
    assert srs.sort is True
    assert srs.index is srs.index
    assert srs.data is ins.data

    # change cell
    ins[1] = 22
    assert srs.data == [1, 22, 3]
    assert srs.index == [0, 1, 5]

    # add a row end
    ins[6] = 4
    assert srs.data == [1, 22, 3, 4]
    assert srs.index == [0, 1, 5, 6]

    # add value in middle
    ins[2] = 12
    assert srs.data == [1, 22, 12, 3, 4]
    assert srs.index == [0, 1, 2, 5, 6]

    # append row
    ins.append_row(7, 55)
    assert srs.data == [1, 22, 12, 3, 4, 55]
    assert srs.index == [0, 1, 2, 5, 6, 7]


def test_from_series_view_breaks():
    # These actions will break the view link between the Series and the ViewSeries

    # changing index
    ins = rc.Series(data=[1, 2, 3], data_name='a', index=[0, 1, 5], sort=True)
    srs = rc.ViewSeries.from_series(ins)
    assert srs.index is ins.index
    assert srs.data is ins.data

    ins.index = [1, 2, 3]
    assert srs.index is not ins.index
    assert srs.data is ins.data

    # sorting index
    ins = rc.Series(data=[1, 2, 3], data_name='a', index=[0, 1, 5], sort=True)
    srs = rc.ViewSeries.from_series(ins)
    assert srs.index is ins.index
    assert srs.data is ins.data

    ins.sort_index()
    assert srs.index is not ins.index
    assert srs.data is not ins.data


def test_value():
    # single int
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8])
    assert srs.value(2) == 7
    assert srs.value(2, int_as_index=True) == 5

    # single int w/offset
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=1)
    assert srs.value(2) == 6
    assert srs.value(2, int_as_index=True) == 5

    # list of values
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=0)
    assert srs.value([2, 3]) == [7, 8]
    assert srs.value([2, 4], int_as_index=True) == [5, 6]

    # list of values w/offset. Note offset has no effect on index
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=1)
    assert srs.value([2, 3]) == [6, 7]
    assert srs.value([2, 4], int_as_index=True) == [5, 6]

    # list of booleans
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=0)
    assert srs.value([False, True, True, False]) == [6, 7]

    # note that offset has no effect on boolean list
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=1)
    assert srs.value([False, True, True, False]) == [6, 7]
    assert srs.value([True, False, False, True]) == [5, 8]

    # slice no offset
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=0)
    assert srs.value(slice(1, 3)) == [6, 7, 8]
    assert srs.value(slice(2, 3)) == [7, 8]
    assert srs.value(slice(-3, -1)) == [6, 7, 8]
    assert srs.value(slice(-3, -2)) == [6, 7]
    assert srs.value(slice(2, 4), int_as_index=True) == [5, 6]

    # slice w/offset
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=1)
    assert srs.value(slice(1, 3)) == [5, 6, 7]
    assert srs.value(slice(2, 3)) == [6, 7]
    assert srs.value(slice(-3, -1)) == [5, 6, 7]
    assert srs.value(slice(-2, 0)) == [6, 7, 8]
    assert srs.value(slice(-3, -2)) == [5, 6]
    assert srs.value(slice(2, 4), int_as_index=True) == [5, 6]

    # slice out of bounds. Uses standard python logic
    # slice w/offset
    srs = rc.ViewSeries([5, 6, 7, 8], index=[2, 4, 6, 8], offset=1)
    assert srs.value(slice(2, 9)) == [6, 7, 8]
    assert srs.value(slice(-30, -1)) == [5, 6, 7]
    assert srs.value(slice(-2, 0)) == [6, 7, 8]
    assert srs.value(slice(-30, -20)) == []

    # lower bound too low
    with pytest.raises(IndexError):
        srs.value(slice(0, 4))

    # end before beginning
    with pytest.raises(IndexError):
        srs.value(slice(4, 2))


def test_get_square_brackets():
    srs = rc.ViewSeries([10, 11, 12], index=['a', 'b', 'c'], sort=False)

    # by index
    assert srs['b'] == 11
    assert srs[['a', 'c']] == [10, 12]
    assert srs['b':'c'] == [11, 12]
    assert srs['a':'b'] == [10, 11]

    # by location
    assert srs[1] == 11
    assert srs[[0, 2]] == [10, 12]
    assert srs[1:2] == [11, 12]
    assert srs[-3:-2] == [10, 11]


def test_get_square_brackets_offset():
    srs = rc.ViewSeries([10, 11, 12], index=['a', 'b', 'c'], sort=False, offset=1)

    # by index
    assert srs['b'] == 11
    assert srs[['a', 'c']] == [10, 12]
    assert srs['b':'c'] == [11, 12]
    assert srs['a':'b'] == [10, 11]

    # by location
    assert srs[1] == 10
    assert srs[2] == 11
    assert srs[3] == 12
    assert srs[-2] == 10
    assert srs[-1] == 11
    assert srs[0] == 12

    assert srs[[0, 2]] == [12, 11]
    assert srs[1:2] == [10, 11]
    assert srs[-3:-2] == [10]
    assert srs[-1:0] == [11, 12]
    assert srs[-2:0] == [10, 11, 12]

    # sort = True
    srs = rc.ViewSeries([10, 11, 12], index=['a', 'b', 'c'], sort=True, offset=1)

    # by index
    assert srs['b'] == 11
    assert srs[['a', 'c']] == [10, 12]
    assert srs['b':'c'] == [11, 12]
    assert srs['a':'b'] == [10, 11]

    # by location
    assert srs[1] == 10
    assert srs[2] == 11
    assert srs[3] == 12
    assert srs[-2] == 10
    assert srs[-1] == 11
    assert srs[0] == 12

    assert srs[[0, 2]] == [12, 11]
    assert srs[1:2] == [10, 11]
    assert srs[-3:-2] == [10]
    assert srs[-1:0] == [11, 12]
    assert srs[-2:0] == [10, 11, 12]

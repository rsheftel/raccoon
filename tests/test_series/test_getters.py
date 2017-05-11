import pytest
import raccoon as rc
from blist import blist


def test_index():
    actual = rc.Series([4, 5, 6], index=['a', 'b', 'c'])
    result = actual.index
    assert result == ['a', 'b', 'c']
    assert isinstance(result, list)

    # test that a view is returned
    result.append('bad')
    assert actual.index == ['a', 'b', 'c', 'bad']

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]
    assert isinstance(result, list)

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]

    assert actual.index_name == 'index'
    actual.index_name = 'new name'
    assert actual.index_name == 'new name'

    actual = rc.Series([4, 5, 6], index=['a', 'b', 'c'], index_name='letters')
    assert actual.index_name == 'letters'


def test_index_blist():
    actual = rc.Series([4, 5, 6], index=['a', 'b', 'c'], use_blist=True)
    result = actual.index
    assert result == ['a', 'b', 'c']
    assert isinstance(result, blist)

    # test that a view is returned
    result.append('bad')
    assert actual.index == ['a', 'b', 'c', 'bad']

    actual.index = [9, 10, 11]
    assert actual.index == [9, 10, 11]
    assert isinstance(result, blist)

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]


def test_index_view():
    data = [4, 5, 6]
    index =['a', 'b', 'c']

    actual = rc.ViewSeries(data, index)
    result = actual.index
    assert result == ['a', 'b', 'c']
    assert isinstance(result, list)

    # test that a view is returned
    assert result is index
    assert result is actual.index

    # modify
    result[1] = 'new'
    assert actual.index == ['a', 'new', 'c']
    assert index == ['a', 'new', 'c']

    # index too long
    with pytest.raises(ValueError):
        actual.index = [1, 3, 4, 5, 6]

    assert actual.index_name == 'index'
    actual.index_name = 'new name'
    assert actual.index_name == 'new name'

    actual = rc.Series([4, 5, 6], index=['a', 'b', 'c'], index_name='letters')
    assert actual.index_name == 'letters'


def test_data():
    data = [4, 5, 6]
    index =['a', 'b', 'c']
    actual = rc.Series(data, index)

    assert isinstance(actual.data, list)
    assert data is not actual.data
    assert actual.data == [4, 5, 6]

    # test data is a view and changes to the .data will corrupt the Series
    new = actual.data
    new[0] = 99
    assert actual.data == new

    new.append(88)
    assert new == [99, 5, 6, 88]
    assert actual.data == [99, 5, 6, 88]

    with pytest.raises(AttributeError):
        actual.data = [4, 5]


def test_data_blist():
    actual = rc.Series([4, 5, 6], index=['a', 'b', 'c'], use_blist=True)
    assert actual.data == [4, 5, 6]
    assert isinstance(actual.data, blist)


def test_data_view():
    data = [4, 5, 6]
    index =['a', 'b', 'c']
    actual = rc.ViewSeries(data, index)

    assert isinstance(actual.data, list)
    assert data is actual.data
    assert actual.data == [4, 5, 6]

    # test data is a copy
    new = actual.data
    new[0] = 99
    assert actual.data == new
    assert data == new

    # changing the data can cause issues
    new.append(88)
    assert new == [99, 5, 6, 88]
    assert actual.data == [99, 5, 6, 88]
    assert actual.index == ['a', 'b', 'c']

    with pytest.raises(AttributeError):
        actual.data = [4, 5]

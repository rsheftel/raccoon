import pytest
import raccoon as rc


def test_validate_index():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df.validate_integrity()

    # index not right length
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9, 11, 12])

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df._index = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        df.validate_integrity()

    # duplicate index
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 10, 9])

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    with pytest.raises(ValueError):
        df.index = [10, 10, 10]

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df._index = [10, 10, 9]
    with pytest.raises(ValueError):
        df.validate_integrity()


def test_validate_columns():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df.validate_integrity()

    # columns not right length
    with pytest.raises(ValueError):
        rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b', 'extra'])

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'])
    df._columns = ['a', 'b', 'extra']
    with pytest.raises(ValueError):
        df.validate_integrity()

    # duplicate columns
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']})
    with pytest.raises(ValueError):
        df.columns = ['dup', 'dup']

    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df._columns = ['dup', 'dup']
    with pytest.raises(ValueError):
        df.validate_integrity()


def test_validate_data():
    df = rc.DataFrame({'a': [2, 1, 3], 'b': ['a', 'c', 'b']}, columns=['a', 'b'], index=[10, 8, 9])
    df.validate_integrity()

    df._data[1] = ['a', 'c']
    assert df.data == [[2, 1, 3], ['a', 'c']]

    with pytest.raises(ValueError):
        df.validate_integrity()

    # validate empty
    df = rc.DataFrame()
    df.validate_integrity()

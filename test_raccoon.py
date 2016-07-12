
import raccoon as rc
import pytest

def test_initialization():
    # solid matrix, no columns, no index
    actual = rc.DataFrame({'a': [1,2,3], 'b': [4,5,6]})
    assert set(tuple(x) for x in actual.values) == {(1,2,3), (4,5,6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == [0, 1, 2]
    
    # solid matrix, no columns, with index
    actual = rc.DataFrame({'a': [1,2,3], 'b': [4,5,6]}, index=['a', 'b', 'c'])
    assert set(tuple(x) for x in actual.values) == {(1,2,3), (4,5,6)}
    assert set(actual.columns) == {'a', 'b'}
    assert actual.index == ['a', 'b', 'c']
    
    # solid matrix, columns, index
    actual = rc.DataFrame({'a': [1,2,3], 'b': [4,5,6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    assert actual.values == [[4, 5, 6], [1, 2, 3]]
    assert actual.columns == ['b', 'a']
    assert actual.index == ['a', 'b', 'c']
    
    
def test_jagged_data():
    actual = rc.DataFrame({'a': [], 'b': [1], 'c': [1, 2], 'd':[1, 2, 3]}, columns=['a', 'b', 'c', 'd'])
    assert actual.values == [[None, None, None], [1, None, None], [1, 2, None], [1, 2, 3]]
    assert actual.columns == ['a', 'b', 'c', 'd']
    assert actual.index == [0, 1, 2]
    
    
def test_empty_initialization():
    actual = rc.DataFrame()
    assert isinstance(actual, rc.DataFrame)
    assert actual.values == [[]]
    assert actual.columns == []
    assert actual.index == []

    actual = rc.DataFrame(columns=['a','b','c'])
    assert actual.values == [[], [], []]
    assert actual.columns == ['a','b','c']
    assert actual.index == []
    
    actual = rc.DataFrame(index=[1, 2, 3])
    assert actual.values == [[None, None, None]]
    assert actual.columns == [1]
    assert actual.index == [1, 2, 3]

    actual = rc.DataFrame(index=[1, 2, 3], columns=['a', 'b'])
    assert actual.values == [[None, None, None], [None, None, None]]
    assert actual.columns == ['a', 'b']
    assert actual.index == [1, 2, 3]


def test_bad_initialization():
    # wrong number in index
    
    # wrong number of columns
    
    # columns does not match dict keys
    
    assert False


def test_columns():
    actual = rc.DataFrame({'a': [1,2,3], 'b': [4,5,6]}, index=['a', 'b', 'c'], columns=['b', 'a'])
    names = actual.columns 
    assert  names == ['b', 'a']
    
    # test copy not view
    names = ['bad', 'bad', 'bad']
    assert  actual.columns  == ['b', 'a']
    
    actual.columns = ['new1', 'new2']
    assert actual.columns == ['new1', 'new2']

    with pytest.raises(AttributeError):
        actual.columns = ['list', 'too', 'long']
    

def test_index():
    assert False
    
    
def test_values():
    assert False

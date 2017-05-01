import pytest
import raccoon as rc


def test_validate_index():
    srs = rc.Series([2, 1, 3], index=[10, 8, 9])
    srs.validate_integrity()

    # index not right length
    with pytest.raises(ValueError):
        rc.Series([2, 1, 3], index=[10, 8, 9, 11, 12])

    srs = rc.Series([2, 1, 3], index=[10, 8, 9])
    with pytest.raises(ValueError):
        srs.index = [1, 2, 3, 4]

    # duplicate index
    with pytest.raises(ValueError):
        rc.Series([2, 1, 3], index=[10, 10, 9])

    srs = rc.Series([2, 1, 3], index=[10, 8, 9])
    with pytest.raises(ValueError):
        srs.index = [10, 10, 10]

    srs = rc.Series([2, 1, 3], index=[10, 8, 9])
    with pytest.raises(ValueError):
        srs.index = [10, 10, 9]

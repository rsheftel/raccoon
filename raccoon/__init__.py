import pkg_resources

from .dataframe import DataFrame
from .series import Series, ViewSeries

__version__ = pkg_resources.get_distribution('raccoon').version
__all__ = ['DataFrame', 'Series', 'ViewSeries']

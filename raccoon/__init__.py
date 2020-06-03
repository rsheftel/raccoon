import pkg_resources

from .dataframe import DataFrame
from .series import Series, ViewSeries

# if running in development there may not be a package
try:
    __version__ = pkg_resources.get_distribution('raccoon').version
except pkg_resources.DistributionNotFound:
    __version__ = 'development'

__all__ = ['DataFrame', 'Series', 'ViewSeries']

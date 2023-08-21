from importlib import metadata

from .dataframe import DataFrame
from .series import Series, ViewSeries

# if running in development there may not be a package
try:
    __version__ = metadata.version('raccoon')
except metadata.PackageNotFoundError:
    __version__ = 'development'

__all__ = ['DataFrame', 'Series', 'ViewSeries']

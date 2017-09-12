
from .dataframe import DataFrame
from .series import Series, ViewSeries
import pkg_resources

__version__ = pkg_resources.get_distribution('raccoon').version

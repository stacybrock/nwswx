"""A simple Python 3 client for the NOAA NWS Wx Forecast API"""

from .api import WxAPI

from .__version__ import (
    __title__, __description__, __version__,
    __author__, __license__, __copyright__
)

from .exceptions import (
    WxAPIException, InvalidFormat
)

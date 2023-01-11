"""Client wrapper for making requests to the NOAA NWS Wx Forecast API"""

import requests

from .__version__ import __title__, __version__
from .format_types import formats
from .exceptions import InvalidFormat, APIError

DEFAULT_API_HOST = 'api.weather.gov'

class NWSWxClient(object):
    def __init__(self, useragent_id, *, api_host=None):
        self._useragent_id = useragent_id

        if api_host is not None:
            self._api_host = api_host
        else:
            self._api_host = DEFAULT_API_HOST

    def _url(self, endpoint):
        """Builds a full URL for the given endpoint"""
        return f"https://{self._api_host}/{endpoint}"

    def _get(self, endpoint, *, query=None, return_format=None):
        """Send GET request to NWS Wx Forecast API"""
        headers = {
            'User-Agent': f"{__title__} {__version__} [{self._useragent_id}]"
        }
        if return_format is not None:
            headers['Accept'] = return_format

        try:
            result = requests.get(self._url(endpoint), query, headers=headers)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if result.headers['Content-Type'] == 'application/problem+json':
                problem = result.json()
                raise(
                    APIError(problem['detail'])
                ) from err
            else:
                raise

        if return_format == formats.JSONLD:
            return result.json()
        else:
            return result.text

"""Client wrapper for making requests to the NOAA NWS Wx Forecast API"""

import requests
import pprint
pp_ = pprint.PrettyPrinter(indent=2)
pp = pp_.pprint

from .__version__ import __title__, __version__
from .utils import is_jsonld
from .exceptions import InvalidFormat

DEFAULT_API_HOST = 'api.weather.gov'
ENDPOINT_FORMATS = {
    'geojson': 'application/geo+json',
    'json-ld': 'application/ld+json',
    'dwml': 'application/vnd.noaa.dwml+xml',
    'oxml': 'application/vnd.noaa.obs+xml',
    'cap': 'application/cap+xml',
    'atom': 'application/atom+xml'
}

class NWSWxClient(object):
    def __init__(self, useragent_id, *, api_host=None):
        self._useragent_id = useragent_id

        if api_host is not None:
            self._api_host = api_host
        else:
            self._api_host = DEFAULT_API_HOST

    def _url(self, endpoint):
        """Builds a full URL for the given endpoint"""
        return "https://{}/{}".format(self._api_host, endpoint)

    def _get(self, endpoint, *, query=None, return_format=None):
        """Send GET request to NWS Wx Forecast API"""
        headers = {
            'User-Agent': "{} {} [{}]".format(__title__, __version__,
                                              self._useragent_id)
        }
        if return_format is not None:
            if return_format.lower() in ENDPOINT_FORMATS:
                headers['Accept'] = ENDPOINT_FORMATS[return_format.lower()]
            else:
                raise(InvalidFormat("Invalid format provided: "
                                    "{}".format(return_format)))

        result = requests.get(self._url(endpoint), query, headers=headers)
        if is_jsonld(return_format):
            return result.json()
        else:
            return result.text

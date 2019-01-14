import functools
import pprint
pp_ = pprint.PrettyPrinter(indent=2)
pp = pp_.pprint

from .client import NWSWxClient
from .exceptions import FormatNotAllowed
from .utils import is_jsonld


def allowed_formats(allowed_formats):
    """Decorator to define allowed formats for a function
    representing an API endpoint. If the function is invoked with the
    'return_format' parameter defined, the parameter value is checked
    against the list of allowed formats, and an error is raised if
    the value is not found.

    Params:
    allowed_formats: list of allowed formats

    Returns the result of the decorated function
    """
    def decorator_check_allowed_formats(func):
        @functools.wraps(func)
        def check_allowed_formats(*args, **kwargs):
            if ('return_format' in kwargs
                    and kwargs['return_format'].lower() not in allowed_formats):
                raise FormatNotAllowed(
                    "'{}' format not allowed for this endpoint, expected "
                    "{}".format(kwargs['return_format'], allowed_formats)
                )
            return func(*args, **kwargs)
        return check_allowed_formats
    return decorator_check_allowed_formats


class WxAPI(NWSWxClient):
    @allowed_formats(['geojson', 'json-ld'])
    def gridpoint(self, wfo, grid_x, grid_y, *, return_format=None):
        """Retrieves raw gridded data"""
        pass # TODO

    @allowed_formats(['geojson', 'json-ld'])
    def point(self, lat, lon, *, return_format=None):
        """Retrieves metadata about a point"""
        return self._get("/points/{},{}".format(lat, lon),
                         return_format=return_format)

    @allowed_formats(['geojson', 'json-ld', 'dwml'])
    def point_forecast(self, lat, lon, *, return_format=None):
        """Retrieves forecast data for a point

        Params:
        lat: latitude, eg. 39.0693
        lon: longitude, eg. -94.6716
        return_format: optional, one of 'GeoJSON', 'JSON-LD', 'DWML'

        Period Dict Keys:
        'number': sequence number
        'name': short name for period, eg. 'Today', 'Monday Night'
        'startTime'
        'endTime'
        'isDaytime': boolean
        'temperature'
        'temperatureUnit': 'F' or 'C'
        'temperatureTrend'
        'windSpeed'
        'windDirection'
        'icon': URL to icon image
        'shortForecast': eg. 'Mostly Clear'
        'detailedForecast'

        Returns a list of period dicts
        """
        result = self._get("/points/{},{}/forecast".format(lat, lon),
                           return_format=return_format)
        if is_jsonld(return_format):
            return result['periods']
        else:
            return result

    @allowed_formats(['geojson', 'json-ld'])
    def point_hourly_forecast(self, lat, lon, *, return_format=None):
        """Retrieves hourly forecast data for a point

        Params:
        lat: latitude, eg. 39.0693
        lon: longitude, eg. -94.6716
        return_format: optional, one of 'GeoJSON', 'JSON-LD'

        Period Dict Keys:
        'number': sequence number
        'name': short name for period, eg. 'Today', 'Monday Night'
        'startTime'
        'endTime'
        'isDaytime': boolean
        'temperature'
        'temperatureUnit': 'F' or 'C'
        'temperatureTrend'
        'windSpeed'
        'windDirection'
        'icon': URL to icon image
        'shortForecast': eg. 'Mostly Clear'
        'detailedForecast'

        Returns a list of period dicts (NOTE: very long-term forecast
        periods do not contain the full set of keys listed above.)
        """
        result = self._get("/points/{},{}/forecast/hourly".format(lat, lon),
                           return_format=return_format)
        if is_jsonld(return_format):
            return result['periods']
        else:
            return result

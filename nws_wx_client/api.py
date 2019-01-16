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

    :param allowed_formats: list of allowed formats

    :returns: The result of the decorated function
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
    """WxAPI class that acts as the central object for interfacing
    with the NWS Weather Forecast API.

    :param useragent_id: identifier to send in useragent, generally
                         an email address
    :param api_host: :emphasis:`optional`, NWS Weather Forecast API host,
                     defaults to :literal:`api.weather.gov`
    """

    @allowed_formats(['geojson', 'json-ld'])
    def gridpoint(self, wfo, grid_x, grid_y, *, return_format=None):
        """Retrieves raw gridded data

        :param wfo: a `Weather Office ID
                    <https://en.wikipedia.org/wiki/List_of_National_Weather_Service_Weather_Forecast_Offices>`_
        :param grid_x: the grid x coordinate
        :param grid_y: the grid y coordinate
        :param return_format: :emphasis:`optional`, one of 'GeoJSON', 'JSON-LD'

        :strong:`Gridded Data Dict Keys:`

        * :literal:`updateTime`
        * :literal:`validTimes`
        * :literal:`geometry`
        * :literal:`elevation`
        * :literal:`forecastOffice`
        * :literal:`gridId`
        * :literal:`gridX`
        * :literal:`gridY`
        * :literal:`temperature`
        * :literal:`dewpoint`
        * :literal:`maxTemperature`
        * :literal:`minTemperature`
        * :literal:`relativeHumidity`
        * :literal:`apparentTemperature`
        * :literal:`heatIndex`
        * :literal:`windChill`
        * :literal:`pressure`
        * :literal:`skyCover`
        * :literal:`windDirection`
        * :literal:`windSpeed`
        * :literal:`windGust`
        * :literal:`weather`
        * :literal:`hazards`
        * :literal:`probabilityOfPrecipitation`
        * :literal:`quantitativePrecipitation`
        * :literal:`iceAccumulation`
        * :literal:`snowfallAmount`
        * :literal:`snowLevel`
        * :literal:`ceilingHeight`
        * :literal:`visibility`
        * :literal:`transportWindSpeed`
        * :literal:`transportWindDirection`
        * :literal:`mixingHeight`
        * :literal:`hainesIndex`
        * :literal:`lightningActivityLevel`
        * :literal:`twentyFootWindSpeed`
        * :literal:`twentyFootWindDirection`
        * :literal:`waveDirection`
        * :literal:`waveHeight`
        * :literal:`wavePeriod`
        * :literal:`wavePeriod2`
        * :literal:`primarySwellHeight`
        * :literal:`primarySwellDirection`
        * :literal:`secondarySwellHeight`
        * :literal:`secondarySwellDirection`
        * :literal:`windWaveHeight`
        * :literal:`dispersionIndex`
        * :literal:`probabilityOfTropicalStormWinds`
        * :literal:`probabilityOfHurricaneWinds`
        * :literal:`potentialOf15mphWinds`
        * :literal:`potentialOf25mphWinds`
        * :literal:`potentialOf35mphWinds`
        * :literal:`potentialOf45mphWinds`
        * :literal:`potentialOf20mphWindGusts`
        * :literal:`potentialOf30mphWindGusts`
        * :literal:`potentialOf40mphWindGusts`
        * :literal:`potentialOf50mphWindGusts`
        * :literal:`potentialOf60mphWindGusts`
        * :literal:`grasslandFireDangerIndex`
        * :literal:`probabilityOfThunder`
        * :literal:`davisStabilityIndex`
        * :literal:`atmosphericDispersionIndex`
        * :literal:`lowVisibilityOccurrenceRiskIndex`
        * :literal:`stability`
        * :literal:`redFlagThreatIndex`

        :returns: If format is 'JSON-LD', a dict of gridded data. Otherwise,
                  a string of gridded data in GeoJSON format.
        """
        return self._get(
            "/gridpoints/{}/{},{}".format(wfo, grid_x, grid_y),
            return_format=return_format
        )

    @allowed_formats(['geojson', 'json-ld'])
    def point(self, lat, lon, *, return_format=None):
        """Retrieves metadata about a point

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of 'GeoJSON', 'JSON-LD'

        :strong:`Point Metadata Dict Keys:`

        * :literal:`geometry`
        * :literal:`cwa`
        * :literal:`forecastOffice`
        * :literal:`gridX`
        * :literal:`gridY`
        * :literal:`forecast`
        * :literal:`forecastHourly`
        * :literal:`forecastGridData`
        * :literal:`observationStations`
        * :literal:`relativeLocation`
        * :literal:`forecastZone`
        * :literal:`county`
        * :literal:`fireWeatherZone`
        * :literal:`timeZone`
        * :literal:`radarStation`

        :returns: If format is 'JSON-LD', a dict of metadata. Otherwise,
                  a string of metadata in GeoJSON format.
        """
        return self._get("/points/{},{}".format(lat, lon),
                         return_format=return_format)

    @allowed_formats(['geojson', 'json-ld', 'dwml'])
    def point_forecast(self, lat, lon, *, return_format=None):
        """Retrieves forecast data for a point

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of 'GeoJSON',
                              'JSON-LD', 'DWML'

        :strong:`Forecast Dict Keys`:

        * :literal:`number` - sequence number
        * :literal:`name` - short name for period, eg. 'Today', 'Monday Night'
        * :literal:`startTime`
        * :literal:`endTime`
        * :literal:`isDaytime` - boolean
        * :literal:`temperature`
        * :literal:`temperatureUnit` - 'F' or 'C'
        * :literal:`temperatureTrend`
        * :literal:`windSpeed`
        * :literal:`windDirection`
        * :literal:`icon` - URL to icon image
        * :literal:`shortForecast` - eg. 'Mostly Clear'
        * :literal:`detailedForecast`

        :returns: If format is 'JSON-LD', a list of dicts containing
                  forecast data. Otherwise, a string containing forecast
                  data in GeoJSON or DWML format.
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

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of 'GeoJSON', 'JSON-LD'

        :strong:`Forecast Dict Keys`:

        * :literal:`number` - sequence number
        * :literal:`name` - short name for period, eg. 'Today', 'Monday Night'
        * :literal:`startTime`
        * :literal:`endTime`
        * :literal:`isDaytime` - boolean
        * :literal:`temperature`
        * :literal:`temperatureUnit` - 'F' or 'C'
        * :literal:`temperatureTrend`
        * :literal:`windSpeed`
        * :literal:`windDirection`
        * :literal:`icon` - URL to icon image
        * :literal:`shortForecast` - eg. 'Mostly Clear'
        * :literal:`detailedForecast`

        :returns: If format is 'JSON-LD', a list of dicts containing
                  forecast data. Otherwise, a string containing forecast
                  data in GeoJSON format.

        .. note:: Very long-term forecast periods do not contain the full
                  set of keys listed above.
        """
        result = self._get("/points/{},{}/forecast/hourly".format(lat, lon),
                           return_format=return_format)
        if is_jsonld(return_format):
            return result['periods']
        else:
            return result

    @allowed_formats(['geojson', 'json-ld'])
    def point_stations(self, lat, lon, *, return_format=None):
        """Retrieves stations nearest to a point in order of distance

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of 'GeoJSON', 'JSON-LD'

        :returns: If format is 'JSON-LD', a list of station URLs. Otherwise,
                  a string containing forecast data in GeoJSON format.
        """
        result = self._get("/points/{},{}/stations".format(lat, lon),
                           return_format=return_format)
        if is_jsonld(return_format):
            return result['observationStations']
        else:
            return result

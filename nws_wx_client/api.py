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
                     defaults to ``api.weather.gov``
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

        * ``updateTime``
        * ``validTimes``
        * ``geometry``
        * ``elevation``
        * ``forecastOffice``
        * ``gridId``
        * ``gridX``
        * ``gridY``
        * ``temperature``
        * ``dewpoint``
        * ``maxTemperature``
        * ``minTemperature``
        * ``relativeHumidity``
        * ``apparentTemperature``
        * ``heatIndex``
        * ``windChill``
        * ``pressure``
        * ``skyCover``
        * ``windDirection``
        * ``windSpeed``
        * ``windGust``
        * ``weather``
        * ``hazards``
        * ``probabilityOfPrecipitation``
        * ``quantitativePrecipitation``
        * ``iceAccumulation``
        * ``snowfallAmount``
        * ``snowLevel``
        * ``ceilingHeight``
        * ``visibility``
        * ``transportWindSpeed``
        * ``transportWindDirection``
        * ``mixingHeight``
        * ``hainesIndex``
        * ``lightningActivityLevel``
        * ``twentyFootWindSpeed``
        * ``twentyFootWindDirection``
        * ``waveDirection``
        * ``waveHeight``
        * ``wavePeriod``
        * ``wavePeriod2``
        * ``primarySwellHeight``
        * ``primarySwellDirection``
        * ``secondarySwellHeight``
        * ``secondarySwellDirection``
        * ``windWaveHeight``
        * ``dispersionIndex``
        * ``probabilityOfTropicalStormWinds``
        * ``probabilityOfHurricaneWinds``
        * ``potentialOf15mphWinds``
        * ``potentialOf25mphWinds``
        * ``potentialOf35mphWinds``
        * ``potentialOf45mphWinds``
        * ``potentialOf20mphWindGusts``
        * ``potentialOf30mphWindGusts``
        * ``potentialOf40mphWindGusts``
        * ``potentialOf50mphWindGusts``
        * ``potentialOf60mphWindGusts``
        * ``grasslandFireDangerIndex``
        * ``probabilityOfThunder``
        * ``davisStabilityIndex``
        * ``atmosphericDispersionIndex``
        * ``lowVisibilityOccurrenceRiskIndex``
        * ``stability``
        * ``redFlagThreatIndex``

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

        * ``geometry``
        * ``cwa``
        * ``forecastOffice``
        * ``gridX``
        * ``gridY``
        * ``forecast``
        * ``forecastHourly``
        * ``forecastGridData``
        * ``observationStations``
        * ``relativeLocation``
        * ``forecastZone``
        * ``county``
        * ``fireWeatherZone``
        * ``timeZone``
        * ``radarStation``

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

        * ``number`` - sequence number
        * ``name`` - short name for period, eg. 'Today', 'Monday Night'
        * ``startTime``
        * ``endTime``
        * ``isDaytime`` - boolean
        * ``temperature``
        * ``temperatureUnit`` - 'F' or 'C'
        * ``temperatureTrend``
        * ``windSpeed``
        * ``windDirection``
        * ``icon`` - URL to icon image
        * ``shortForecast`` - eg. 'Mostly Clear'
        * ``detailedForecast``

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

        * ``number`` - sequence number
        * ``name`` - short name for period, eg. 'Today', 'Monday Night'
        * ``startTime``
        * ``endTime``
        * ``isDaytime`` - boolean
        * ``temperature``
        * ``temperatureUnit`` - 'F' or 'C'
        * ``temperatureTrend``
        * ``windSpeed``
        * ``windDirection``
        * ``icon`` - URL to icon image
        * ``shortForecast`` - eg. 'Mostly Clear'
        * ``detailedForecast``

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

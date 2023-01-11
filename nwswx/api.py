import functools

from .client import NWSWxClient
from .format_types import formats
from .exceptions import FormatNotAllowed


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
                    and kwargs['return_format'] not in allowed_formats):
                raise FormatNotAllowed(
                    f"'{kwargs['return_format']}' format not allowed for this "
                    f"endpoint, expected {allowed_formats}"
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

    @allowed_formats([formats.GeoJSON, formats.JSONLD])
    def gridpoint(self, wfo, grid_x, grid_y, *, return_format=None):
        """Retrieves raw gridded data

        :param wfo: a `Weather Office ID
                    <https://en.wikipedia.org/wiki/List_of_National_Weather_Service_Weather_Forecast_Offices>`_
        :param grid_x: the grid x coordinate
        :param grid_y: the grid y coordinate
        :param return_format: :emphasis:`optional`, one of ``GeoJSON``,
                              ``JSONLD``

        :strong:`Gridded Data Dict Keys:`

        * ``@context``
        * ``@id``
        * ``@type``
        * ``apparentTemperature``
        * ``atmosphericDispersionIndex``
        * ``ceilingHeight``
        * ``davisStabilityIndex``
        * ``dewpoint``
        * ``dispersionIndex``
        * ``elevation``
        * ``forecastOffice``
        * ``geometry``
        * ``grasslandFireDangerIndex``
        * ``gridId``
        * ``gridX``
        * ``gridY``
        * ``hainesIndex``
        * ``hazards``
        * ``heatIndex``
        * ``iceAccumulation``
        * ``lightningActivityLevel``
        * ``lowVisibilityOccurrenceRiskIndex``
        * ``maxTemperature``
        * ``minTemperature``
        * ``mixingHeight``
        * ``potentialOf15mphWinds``
        * ``potentialOf20mphWindGusts``
        * ``potentialOf25mphWinds``
        * ``potentialOf30mphWindGusts``
        * ``potentialOf35mphWinds``
        * ``potentialOf40mphWindGusts``
        * ``potentialOf45mphWinds``
        * ``potentialOf50mphWindGusts``
        * ``potentialOf60mphWindGusts``
        * ``pressure``
        * ``primarySwellDirection``
        * ``primarySwellHeight``
        * ``probabilityOfHurricaneWinds``
        * ``probabilityOfPrecipitation``
        * ``probabilityOfThunder``
        * ``probabilityOfTropicalStormWinds``
        * ``quantitativePrecipitation``
        * ``redFlagThreatIndex``
        * ``relativeHumidity``
        * ``secondarySwellDirection``
        * ``secondarySwellHeight``
        * ``skyCover``
        * ``snowLevel``
        * ``snowfallAmount``
        * ``stability``
        * ``temperature``
        * ``transportWindDirection``
        * ``transportWindSpeed``
        * ``twentyFootWindDirection``
        * ``twentyFootWindSpeed``
        * ``updateTime``
        * ``validTimes``
        * ``visibility``
        * ``waveDirection``
        * ``waveHeight``
        * ``wavePeriod``
        * ``wavePeriod2``
        * ``weather``
        * ``windChill``
        * ``windDirection``
        * ``windGust``
        * ``windSpeed``
        * ``windWaveHeight``

        :returns: If format is ``JSONLD``, a dict of gridded data. Otherwise,
                  a string of gridded data in GeoJSON format.
        """
        return self._get(f"gridpoints/{wfo}/{grid_x},{grid_y}",
                         return_format=return_format)

    @allowed_formats([formats.GeoJSON, formats.JSONLD])
    def point(self, lat, lon, *, return_format=None):
        """Retrieves metadata about a point

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of ``GeoJSON``,
                              ``JSONLD``

        :strong:`Point Metadata Dict Keys:`

        * ``@context``
        * ``@id``
        * ``@type``
        * ``county``
        * ``cwa``
        * ``fireWeatherZone``
        * ``forecast``
        * ``forecastGridData``
        * ``forecastHourly``
        * ``forecastOffice``
        * ``forecastZone``
        * ``geometry``
        * ``gridX``
        * ``gridY``
        * ``observationStations``
        * ``radarStation``
        * ``relativeLocation``
        * ``timeZone``

        :returns: If format is ``JSONLD``, a dict of metadata. Otherwise,
                  a string of metadata in GeoJSON format.
        """
        return self._get(f"points/{lat},{lon}", return_format=return_format)

    @allowed_formats([formats.GeoJSON, formats.JSONLD, formats.DWML])
    def point_forecast(self, lat, lon, *, return_format=None):
        """Retrieves forecast data for a point

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of ``GeoJSON``,
                              ``JSONLD``, ``DWML``

        :strong:`Forecast Dict Keys`:

        * `@`context``
        * ``elevation``
        * ``forecastGenerator``
        * ``generatedAt``
        * ``geometry``
        * ``periods`` - a dict of periods (see period keys below)
        * ``units``
        * ``updateTime``
        * ``updated``
        * ``validTimes``

        :strong:`Period Dict Keys`:

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

        :returns: If format is ``JSONLD``, a dict containing forecast data.
                  Otherwise, a string containing forecast data in GeoJSON
                  or DWML format.
        """
        point = self.point(lat, lon, return_format=formats.JSONLD)
        endpoint = (f"gridpoints/{point['gridId']}/"
                    f"{point['gridX']},{point['gridY']}/forecast")
        return self._get(endpoint, return_format=return_format)

    @allowed_formats([formats.GeoJSON, formats.JSONLD])
    def point_hourly_forecast(self, lat, lon, *, return_format=None):
        """Retrieves hourly forecast data for a point

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of ``GeoJSON``,
                              ``JSONLD``

        :strong:`Forecast Dict Keys`:

        * `@`context``
        * ``elevation``
        * ``forecastGenerator``
        * ``generatedAt``
        * ``geometry``
        * ``periods`` - a dict of periods (see period keys below)
        * ``units``
        * ``updateTime``
        * ``updated``
        * ``validTimes``

        :strong:`Period Dict Keys`:

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

        :returns: If format is ``JSONLD``, a list of dicts containing
                  forecast data. Otherwise, a string containing forecast
                  data in GeoJSON format.

        .. note:: Very long-term forecast periods do not contain the full
                  set of keys listed above.
        """
        return self._get(f"points/{lat},{lon}/forecast/hourly",
                         return_format=return_format)

    @allowed_formats([formats.GeoJSON, formats.JSONLD])
    def point_stations(self, lat, lon, *, return_format=None):
        """Retrieves stations nearest to a point in order of distance

        :param lat: latitude, eg. 39.0693
        :param lon: longitude, eg. -94.6716
        :param return_format: :emphasis:`optional`, one of ``GeoJSON`` or
                              ``JSONLD``

        :returns: If format is ``JSONLD``, a list of station URLs. Otherwise,
                  a string containing forecast data in GeoJSON format.
        """
        return self._get(f"points/{lat},{lon}/stations",
                         return_format=return_format)

    @allowed_formats([formats.JSONLD, formats.ATOM])
    def alerts(self, params=None, *, return_format=None):
        """Retrieves a list of alerts, optionally filtered by parameters

        :param params: a dict of parameters
        :param return_format: :emphasis:`optional`, one of ``JSONLD`` or
                              ``ATOM``

        :strong:`Filter Parameters:`

        This list is included verbatim from the `NWS Weather Forecast API
        documentation <https://forecast-v3.weather.gov/documentation>`_.

        * ``active`` - active alerts (1 or 0)
        * ``start`` - start time (ISO8601DateTime)
        * ``end`` - end time (ISO8601DateTime)
        * ``status`` - event status (alert, update, cancel)
        * ``type`` - event type (list forthcoming)
        * ``zone_type`` - zone type (land or marine)
        * ``point`` - point (latitude,longitude)
        * ``region`` - region code (list forthcoming)
        * ``state`` - state/marine code (list forthcoming)
        * ``zone`` - zone ID (forecast or county, list forthcoming)
        * ``urgency`` - urgency (expected, immediate)
        * ``severity`` - severity (minor, moderate, severe)
        * ``certainty`` - certainty (likely, observed)
        * ``limit`` - limit (an integer)

        :strong:`Examples`::

          import nwswx
          nws = nwswx.WxAPI('test@email.com')
          nws.alerts({'point': '39.0693,-94.6716'})
          nws.alerts({'point': '39.0693,-94.6716'},
                     return_format=nwswx.formats.JSONLD)

        :returns: If format is ``JSONLD``, a dict of alerts. Otherwise,
                  a string containing alerts in ATOM format.
        """
        if params is None:
            params = {}

        return self._get('alerts', query=params, return_format=return_format)

    @allowed_formats([formats.JSONLD, formats.ATOM])
    def active_alerts(self, params=None, *, return_format=None):
        """Retrieves a list of active alerts, optionally filtered by
        parameters

        :param params: a dict of parameters
        :param return_format: :emphasis:`optional`, one of ``JSONLD`` or
                              ``ATOM``

        :strong:`Filter Parameters:`

        This list is included verbatim from the `NWS Weather Forecast API
        documentation <https://forecast-v3.weather.gov/documentation>`_.

        * ``status`` - event status (alert, update, cancel)
        * ``type`` - event type (list forthcoming)
        * ``zone_type`` - zone type (land or marine)
        * ``point`` - point (latitude,longitude)
        * ``region`` - region code (list forthcoming)
        * ``state`` - state/marine code (list forthcoming)
        * ``zone`` - zone ID (forecast or county, list forthcoming)
        * ``urgency`` - urgency (expected, immediate)
        * ``severity`` - severity (minor, moderate, severe)
        * ``certainty`` - certainty (likely, observed)
        * ``limit`` - limit (an integer)

        :strong:`Examples`::

          import nwswx
          nws = nwswx.WxAPI('test@email.com')
          nws.active_alerts({'point': '39.0693,-94.6716'})
          nws.active_alerts({'point': '39.0693,-94.6716'},
                            return_format=nwswx.formats.JSONLD)

        :returns: If format is ``JSONLD``, a dict of alerts. Otherwise, a
                  string containing alerts in ATOM format.
        """
        if params is None:
            params = {}

        return self._get('alerts/active', query=params,
                         return_format=return_format)

    @allowed_formats([formats.GeoJSON, formats.JSONLD, formats.CAP])
    def alert(self, alert_id, *, return_format=None):
        """Retrieves details for a specific alert

        :param alert_id: an alert ID provided by another endpoint, eg.
                         ``NWS-IDP-PROD-2202530-2064731``
        :param return_format: :emphasis:`optional`, one of ``JSONLD``, ``CAP``,
                              or ``GeoJSON``

        :strong:`Examples`::

          import nwswx
          nws = nwswx.WxAPI('test@email.com')
          nws.alert('NWS-IDP-PROD-2202530-2064731')
          nws.alert('NWS-IDP-PROD-2202530-2064731',
                    return_format=nwswx.formats.JSONLD)

        :returns: If format is ``JSONLD``, a dict containing the alert details.
                  If format is ``CAP``, a string containing the alert in CAP
                  format. Otherwise, a string containing the alert in GeoJSON
                  format.

        .. note:: GeoJSON is a supported format for this endpoint despite
                  the `API documentation
                  <https://forecast-v3.weather.gov/documentation>`_
                  saying otherwise.
        """
        return self._get(f"alerts/{alert_id}", return_format=return_format)

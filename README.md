# nws-wx-client

A Python 3 client for retrieving data from the [NWS Weather Forecast API](https://forecast-v3.weather.gov/documentation).

## Requirements

* Python 3.4+
* [Requests](http://docs.python-requests.org)

### Package Build Requirements

The full list of packages required to build this module can be found in `requirements.txt`

## Documentation

Full documentation, including examples and an API reference: http://nws-wx-client.readthedocs.io

## Examples

Get forecast for a point in GeoJSON format:
```
>>> import nws_wx_client
>>> nws = nws_wx_client.WxAPI('your@email.com')
>>> forecast = nws.point_forecast(39.0693, -94.6716)
>>> print(forecast)
{
    "@context": [
        "https://raw.githubusercontent.com/geojson/geojson-ld/master/contexts/geojson-base.jsonld",
        {
            "wx": "https://api.weather.gov/ontology#",
            "geo": "http://www.opengis.net/ont/geosparql#",
            "unit": "http://codes.wmo.int/common/unit/",
            "@vocab": "https://api.weather.gov/ontology#"
        }
    ], ...
```

Get forecast for a point in JSON-LD format:
```
>>> import nws_wx_client
>>> nws = nws_wx_client.WxAPI('your@email.com')
>>> forecast = nws.point_forecast(39.0693, -94.6716, return_format='JSON-LD')
>>> print(forecast)
[{'number': 1, 'name': 'Tonight', 'startTime': '2019-01-13T22:00:00-08:00', 'endTime':
'2019-01-14T06:00:00-08:00', 'isDaytime': False, 'temperature': 28, 'temperatureUnit':
'F', 'temperatureTrend': None, 'windSpeed': '2 to 6 mph', 'windDirection': 'N',
'icon': 'https://api.weather.gov/icons/land/night/few?size=medium', 'shortForecast':
'Mostly Clear', 'detailedForecast': 'Mostly clear, with a low around 28. North wind 2
to 6 mph.'}, ...
```

## Limitations, of Which There Are Many

* Most endpoints remain unimplemented and are on the TODO list.

### TODO Endpoints

* `/stations`
* `/stations/{stationId}`
* `/stations/{stationId}/observations`
* `/stations/{stationId}/observations/current`
* `/stations/{stationId}/observations/{recordId}`
* `/products/{productId}`
* `/products/types`
* `/products/types/{typeId}`
* `/products/types/{typeId}/locations`
* `/products/types/{typeId}/locations/{locationId}`
* `/products/locations`
* `/products/locations/{locationId}/types`
* `/offices/{officeId}`
* `/zones/{type}/{zoneId}`
* `/zones/{type}/{zoneId}/forecast`
* `/alerts?{parameters}`
* `/alerts/active`
* `/alerts/{alertId}`
* `/alerts/active/count`
* `/alerts/active/zone/{zoneId}`
* `/alerts/active/area/{area}`
* `/alerts/active/region/{region}`
